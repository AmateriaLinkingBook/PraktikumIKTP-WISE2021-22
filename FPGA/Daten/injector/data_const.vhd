-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file data_const.vhd
--! @brief provides raw data
--! @author: Philipp Horn <philipp.horn@cern.ch>
--------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity data_const is
  generic (
    bit_width : positive := 14
  );
  port (
    clk     : in std_logic;
    sig_i   : in std_logic;
    data_o  : out signed(bit_width-1 downto 0) := (others => '0')
  );
end data_const;

----------------------------------------------------------------------

architecture arch of data_const is

  type v_uns_t is array (natural range <>) of signed(bit_width-1 downto 0);
  constant data: v_uns_t := (
    to_signed(0,bit_width),
    to_signed(3600,bit_width),
    to_signed(7000,bit_width),
    to_signed(5820,bit_width),
    to_signed(3280,bit_width),
    to_signed(1210,bit_width),
    to_signed(-70,bit_width),
    to_signed(-770,bit_width),
    to_signed(-1150,bit_width),
    to_signed(-1330,bit_width),
    to_signed(-1420,bit_width),
    to_signed(-1470,bit_width),
    to_signed(-1500,bit_width),
    to_signed(-1510,bit_width),
    to_signed(-1520,bit_width),
    to_signed(-1520,bit_width),
    to_signed(-1520,bit_width),
    to_signed(-1510,bit_width),
    to_signed(-1510,bit_width),
    to_signed(-1450,bit_width),
    to_signed(-1120,bit_width),
    to_signed(-720,bit_width),
    to_signed(-390,bit_width),
    to_signed(-230,bit_width),
    to_signed(-100,bit_width),
    to_signed(-40,bit_width),
    to_signed(-30,bit_width),
    to_signed(-20,bit_width),
    to_signed(-10,bit_width)
  );

  signal i : natural := 0;

begin

  data_in_proc: process(clk)
  begin
    if rising_edge(clk) then
      if (sig_i = '1') or (i /= 0) then
        if i = data'high then
          i <= 0;
        else
          i <= i + 1;
        end if;
      end if;
    end if;
  end process data_in_proc;

  data_o <= data(i);

end arch;
