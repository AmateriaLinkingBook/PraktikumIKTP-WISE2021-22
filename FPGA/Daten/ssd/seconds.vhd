-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file seconds.vhd
--! @brief displays a seconds counter on one seven segment display (ssd)
--! @author: Philipp Horn <philipp.horn@cern.ch>
--! @details: This module uses single_disp and a 50 MHz clock to count and
--!           display a second counter
--------------------------------------------------------------------------------

library IEEE;
use     IEEE.std_logic_1164.ALL;
use     IEEE.numeric_std.ALL;

entity seconds is
  generic (
    counter_max : positive := 50_000_000;
    invert    : boolean := true
  );
  port (
    clk : in  std_logic;
    ss_d1_o : out std_logic_vector(6 downto 0) := (others => '0')
  );
end seconds;

architecture arch of seconds is

  -- increased with every second
  signal sec:integer := 0;
  -- increased with every rising clock
  signal counter:integer := 0;
  
  signal B : signed (4 downto 0) := (others => '0');

begin
  process_label: process(clk)
  begin
    if rising_edge(clk) then
      counter <= counter + 1;
      if (counter + 1) = counter_max then
        if sec = 9 then
          sec <= 0;
          counter <= 0;
          B <= to_signed(0, 5);
        else
          sec <= sec + 1;
          counter <= 0;
          B <= to_signed(sec + 1, 5);
        end if;
      end if;
      
    end if;
  end process process_label;

  map_label: entity work.single_disp
  generic map(
    invert => invert
  )
  port map(
    number_i => B,
    seg_o => ss_d1_o
  );

end arch;
