-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file max_find.vhd
--! @brief outputs maximum value "data_o" of "data_i"; "start_i" resets maximum
--! @author: Philipp Horn <philipp.horn@cern.ch>
--------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity max_find is
  generic (
    -- signals, which are declared here can be used in the port definition
    bit_width : integer := 14
  );
  port (
    clk     : in  std_logic;
    start_i : in  std_logic;
    data_i  : in  signed(bit_width-1 downto 0);
    data_o  : out signed(bit_width-1 downto 0) := (others => '0')
  );
end max_find;

architecture arch of max_find is

  signal reg : signed(bit_width-1 downto 0) := (others => '0');
begin
  process_label: process(clk)
  begin
    if rising_edge(clk) then
      if start_i = '1' then
        reg <= (others => '0');
      elsif data_i > reg then
        reg <= data_i;
      end if;
    end if;
  end process process_label;

  data_o <= reg;

end arch;
