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
--   0.2 // March, 10 2019
--     changed to simple uart version
--   0.1 // February, 22 2019
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

entity injector is
  generic (
    OFFSET      : positive  := 1024;
    BIT_WIDTH   : positive  := 14;
    SAMPLES_MAX : positive  := 32;
    UART_DBIT   : positive  := 8;    -- uart data bits in uart communication
    SIMULATE    : boolean  := true
  );
  port (
    clk_50  : in  std_logic;
    btn_rst : in  std_logic;

    rx     : in  std_logic;  -- uart serial receive data line
    tx     : out std_logic;  -- uart serial transmit data line

    start  : in  std_logic;
    leds   : out std_logic_vector(1 downto 0);   -- status LEDs 0: ready, 1: armed

    data_valid : out std_logic;
    data_out   : out signed(BIT_WIDTH - 1 downto 0) := (others => '0')
  );
end injector;


architecture arch of injector is

  signal rst_v     : std_logic_vector(2 downto 0) := (others => '1');
  signal rst_50    : std_logic := '1';

  signal data_rx_frame_error : std_logic := '0';
  signal data_rx_valid       : std_logic := '0';
  signal data_rx             : std_logic_vector(UART_DBIT - 1 downto 0) := (others => '0');

 begin

  -- extend and synchronize global reset to common 50 MHz clock
  process(btn_rst, clk_50) begin
    if btn_rst = '1' then
      rst_v <= (others => '1');
    elsif rising_edge(clk_50) then
      rst_v <= rst_v(rst_v'left - 1 downto 0) & '0';
    end if;
  end process;

  rst_50       <= rst_v(rst_v'left);


  uart_inst: entity work.uart
    generic map (
      CLK_FREQ    => 50e6,
      BAUD_RATE   => 115200,
      PARITY_BIT  => "none"
    )
    port map (
      clk    => clk_50,
      rst    => rst_50,

      -- serial uart signal lines
      uart_rxd       => rx,
      uart_txd       => tx,

      -- receive data uart interface
      frame_error => data_rx_frame_error,         -- read from uart
      data_vld    => data_rx_valid,
      data_out    => data_rx,

      -- transmit data
      busy        => open,
      data_send   => '0',             -- don't write to uart
      data_in     => (others => '0')  -- no output data
    );       


  get_gen: if not SIMULATE generate
    getData_inst : entity work.getData
      generic map (
        OFFSET     => OFFSET,
        BIT_WIDTH  => BIT_WIDTH
      )
      port map (
        clk   => clk_50,
        rst   => rst_50,

	start => start,
	leds  => leds,

	-- data stream output 
        data_out_valid => data_valid,
        data_out       => data_out,

        -- uart reads
        data_in_frame_error => data_rx_frame_error,
        data_in_valid       => data_rx_valid,
        data_in             => data_rx
    );
  end generate;

  con_gen: if SIMULATE generate
    const_inst: entity work.data_const
    generic map(
      bit_width => bit_width
    )
    port map (
      clk   => clk_50,
      sig_i => start,
      data_o => data_out
    );
  end generate;

end arch;
