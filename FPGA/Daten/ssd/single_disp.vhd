-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file single_disp.vhd
--! @brief translates a single digit into a seven segment display vector
--! @author: Philipp Horn <philipp.horn@cern.ch>
--! @details: This module inputs a four bit signed number. This is translated
--!           to a seven bit standard logic vector. Every bit of this vector
--!           corresponds to a single segement of the ssd.
--!           The input of numbers 0-9 show the correct number on the display.
--!           Any other input only asserts the middle segment.
--!           A generic gives the possibility to invert the output depending
--!           on hardware configuration.
--------------------------------------------------------------------------------

library IEEE;
use     IEEE.std_logic_1164.ALL;
use     IEEE.numeric_std.ALL;

entity single_disp is
  generic(
    -- definition of generic including the default value "false"
    invert : boolean := false
  );
  port(
    number_i  : in  signed(4 downto 0);
    seg_o     : out std_logic_vector(6 downto 0));
end entity;

architecture arch of single_disp is
  signal seg_s : std_logic_vector(6 downto 0);
begin

  -- seg_s is assigned depending on number_i
  with number_i select
    seg_s <=  "0111111" when "00000",
              "0000110" when "00001",
              "1011011" when "00010",
              "1001111" when "00011",
              "1100110" when "00100",
              "1101101" when "00101",
              "1111101" when "00110",
              "0000111" when "00111",
              "1111111" when "01000",
              "1101111" when "01001",
              "1000000" when others;

  -- seg_s is inverted when generic is set appropriately
  seg_o <=  not seg_s when invert else
            seg_s;

end arch;
