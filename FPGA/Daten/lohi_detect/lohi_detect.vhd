-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file lohi_detect.vhd
--! @brief outputs a single high signal on a rising edge of "sig_i"
--! @author: Philipp Horn <philipp.horn@cern.ch>
--------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;

entity lohi_detect is
port (
  clk   : in  std_logic;
  sig_i : in  std_logic;
  sig_o : out std_logic := '0'
);
end lohi_detect;

architecture arch of lohi_detect is


  signal reg : std_logic := '0';
begin

  process_label: process(clk)
  begin
    if rising_edge(clk) then
      sig_o <= sig_i and (not reg);
      reg <= sig_i;
    end if;
  end process process_label;

end arch;
