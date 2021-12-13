--
-- ============================================================================
-- Author:
--   Rainer Hentges <rainer.hentges@cern.ch>
--
-- Package:
--   terascale-DWS
--
-- Description:
--   Note: run simulation for at least 20 ms
--   to do: handle received data while sending
--
-- Versions:
--   0.3 // March, 10 2019
--     changed to uart_simple without fifo
--     simplified state machine with states: idle, waitHigh, and sendData
--   0.2 // February, 18 2019
--     buffer added, 
--     new sates: sendData, clearData
--   0.1 // February, 5 2019
--     initial version
--
-- License:
-- ============================================================================
-- Copyright 2019 Rainer Hentges
--                Technical University of Dresden - Germany,
--                Institute for Nuclear and Particle Physics
--                Experimental Particle Physics
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--    http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--
-- ============================================================================


library IEEE;
  use IEEE.std_logic_1164.all;
  use IEEE.numeric_std.all;

entity getData is
  generic (
    OFFSET      : positive := 1024;
    BIT_WIDTH   : natural := 14;
    SAMPLES_MAX : natural := 32
  );
  port (
    clk    : in  std_logic;
    rst    : in  std_logic;

    start  : in  std_logic;
    leds   : out std_logic_vector(1 downto 0);   -- status LEDs 0: ready, 1: armed

		-- data_out port will stream SAMPLES_MAX data samples at start
		data_out_valid : out std_logic;
    data_out       : out signed(BIT_WIDTH - 1 downto 0) := (others => '0');
    
	  -- data in, data from uart
    data_in_frame_error : in std_logic;          -- presently not used
    data_in_valid       : in std_logic;
    data_in             : in std_logic_vector(BIT_WIDTH / 2 downto 0)
  );
end getData;


architecture arch of getData is

  signal data_low  : unsigned(BIT_WIDTH / 2 - 1 downto 0) := (others => '0');
  signal data_uns  : unsigned(BIT_WIDTH - 1 downto 0) := (others => '0');

  signal valid_low : boolean := false;
  signal ready     : boolean := false;
  signal armed     : boolean := true;     -- power up as an armed device

  type buffer_t is array (natural range <>) of unsigned(BIT_WIDTH - 1 downto 0);
  signal sample_counter : natural range 0 to SAMPLES_MAX := 0;  -- is also used as address 
  signal data_buff      : buffer_t (0 to SAMPLES_MAX - 1) := (others => (others => '0'));

  type state_type is (
    idle,
    waitHigh,
    sendData
  );

  signal state : state_type := idle;

begin

  -- drive the status leds
  leds(0) <= '1' when ready else '0';
  leds(1) <= '1' when armed else '0';


  ----------------------------------------------------------
  --  read from fifo, buffer and send to data_o at start  --
  ----------------------------------------------------------
 
  data_fsm : process(clk)
    
  begin

    if rising_edge(clk) then

      if rst = '1' then     -- synchronous reset
 
        state <= idle;

        data_out_valid <= '0';  -- will be overwritten at sendData state
        data_uns       <= (others => '0');

        ready          <= false;
        armed          <= true;     -- start over with an armed device

        sample_counter <= 0;
        data_buff      <= (others => to_unsigned(OFFSET, BIT_WIDTH));

      else

        -- set default values, might be overwritten below
        data_out_valid  <= '0';
        data_uns <= to_unsigned(OFFSET, BIT_WIDTH);

        case state is

          --------------------------------
          --  idle state                --
          --  jump to dedicated states  --
          --------------------------------

          when idle =>
            data_low       <= (others => '0');
            valid_low      <= false;

            if (start = '1') and ready then            -- send if data was successfully loaded
              state <= sendData;
              sample_counter <= 0;
            elsif armed and (data_in_valid = '1') then -- armed and data in valid
              data_low   <= unsigned(data_in(BIT_WIDTH / 2 - 1 downto 0)); -- get low byte
              valid_low  <= true;
              state      <= waitHigh;
              ready      <= false;
            else                                       -- data in not valid or not armed
              state <= idle;
            end if;


          -----------------------------------------------------------------
          --  receive data                                               --
          --  concatenate two uart data packets to one ADC sample value  --
          --  and write it to a buffer                                   --
          -----------------------------------------------------------------

          when waitHigh =>
            if ( data_in_valid = '1') and (data_in(bit_width / 2) = '1') and (valid_low = true) then
              data_buff(sample_counter) <= unsigned(data_in(BIT_WIDTH / 2 - 1 downto 0)) & data_low;
              if sample_counter = (SAMPLES_MAX - 1) then
                ready           <= true;
                armed           <= false;
                sample_counter  <= 0;
              else
                sample_counter  <= sample_counter + 1;
              end if;
            state <= idle;
            end if;


          -----------------------------------------------------------------
          --  send data                                                  --
          --  take data from buffer and send it as a stream to data out  --
          -----------------------------------------------------------------

          when sendData =>
            data_out_valid <= '1';
            data_uns       <= data_buff(sample_counter);
            sample_counter <= sample_counter + 1;

            if sample_counter >= (SAMPLES_MAX - 1) then
              armed <= true;
              state <= idle;
              sample_counter <= 0;
            end if;

        end case;

      end if;  -- rst
    end if;    -- clk

  end process data_fsm;

  data_out <= signed(std_logic_vector(data_uns)) - OFFSET;

end arch;
