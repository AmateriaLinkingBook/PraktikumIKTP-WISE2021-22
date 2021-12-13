-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file example.vhd
--! @brief outputs a single high signal on a falling edge of "sig_i"
--! @author: Philipp Horn <philipp.horn@cern.ch>
--------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;

entity example is
  port (
    input1 : in  std_logic;
    input2 : in  std_logic;
    output : out std_logic := '0'
  );
end entity;

architecture arch of example is
  signal internal : std_logic := '0';
begin

  internal <= input1 and input2;
  output <= not internal;

end arch;

