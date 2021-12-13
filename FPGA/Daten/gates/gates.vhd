-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file gates.vhd
--! @brief outputs a single high signal on a falling edge of "sig_i"
--! @author: Philipp Horn <philipp.horn@cern.ch>
--------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;

entity gates is
port (
  sw0_i   : in  std_logic;
  sw1_i   : in  std_logic;
  sw2_i   : in  std_logic;
  btn0_i  : in  std_logic;
  led0_o  : out std_logic;
  led1_o  : out std_logic;
  led2_o  : out std_logic
);
end gates;

architecture arch of gates is
begin
  led0_o <= (sw0_i and sw1_i) and sw2_i;
  led1_o <= (sw0_i and sw1_i) or (sw1_i and sw2_i) or (sw0_i and sw2_i);
  led2_o <= (sw2_i and (not btn0_i));
end arch;
