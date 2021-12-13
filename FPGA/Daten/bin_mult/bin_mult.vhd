-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file bin_mult.vhd
--! @brief adding two input vectors via logic gates
--! @author: Philipp Horn <philipp.horn@cern.ch>
--------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;

entity bin_mult is
  generic(
    bit_length : integer := 6
  );
  port (
    clk   : in  std_logic;
    a     : in  std_logic_vector(bit_length-1 downto 0);
    b     : in  std_logic_vector(bit_length-1 downto 0);
    c     : out std_logic_vector(2*bit_length-1 downto 0) := (others => '0')
  );
end entity;

architecture arch of bin_mult is

  type matrix_t is array (natural range <>) of std_logic_vector(2*bit_length-2 downto 0);
  signal matrix_s : matrix_t(bit_length-1 downto 0) := (others => (others => '0'));

  signal j : integer := 0;

  signal row    : std_logic_vector(2*bit_length-2 downto 0) := (others => '0');
  signal c_temp : std_logic_vector(2*bit_length-1 downto 0) := (others => '0');

begin


end arch;
