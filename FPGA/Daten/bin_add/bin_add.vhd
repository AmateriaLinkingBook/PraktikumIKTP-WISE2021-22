-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file bin_add.vhd
--! @brief adding two input vectors via logic gates
--! @author: Philipp Horn <philipp.horn@cern.ch>
--------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;

entity bin_add is
  generic(
    bit_length : integer := 10
  );
  port (
    clk : in  std_logic;
    a   : in  std_logic_vector(bit_length-1 downto 0);
    b   : in  std_logic_vector(bit_length-1 downto 0);
    c   : out std_logic_vector(bit_length downto 0) := (others => '0')
  );
end entity;

architecture arch of bin_add is
  signal carry  : std_logic_vector (bit_length downto 0) := (others => '0');
  signal c_temp : std_logic_vector (bit_length downto 0) := (others => '0');
begin


end arch;
