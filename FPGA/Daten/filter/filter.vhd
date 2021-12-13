-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file filter.vhd
--! @brief simple filter
--! @author: Philipp Horn <philipp.horn@cern.ch>
--! @details: This module implements a filter.
--------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity filter is
  generic (
    -- signals, which are declared here can be used in the port definition
    bit_width : positive := 14
  );
  port (
    clk     : in  std_logic;
    data_i  : in  signed(bit_width-1 downto 0);
    data_o  : out signed(bit_width-1 downto 0) := (others => '0')
  );
end entity;

architecture arch of filter is

  -- procedure to avoid calculation with fixed comma digits:
    -- constant coefficients are multiplied with 2^n to get integer values
    -- lower n bits of the result are omitted (same as division by 2^n)

  -- number of bits the coefficients were shifted to the right
  -- the result has to be shifted to the left by the same amount at the end
  constant shif : natural := 15;

  type const_t is array (natural range <>) of integer;
  constant c : const_t(1 to 6) := (
    -9379,  -- c(1)
    17867,  -- c(2)
    44585,  -- c(3)
    -68495, -- c(4)
    36820,  -- c(5)
    -8483   -- c(6)
  );

  signal data_uns : signed(bit_width+shif-1 downto 0) := (others => '0');

  type buf_type is array (natural range <>) of integer;
  signal buf:buf_type(4 downto 0);
  
begin
  
  process_label: process(clk)
  variable par_sum : integer;
  begin
    if rising_edge(clk) then
      buf(0) <= to_integer(data_i);
      for i in 1 to 4 loop
        buf(i) <= buf(i-1);
      end loop;
      
      par_sum := c(1) * to_integer(data_i);
      
      for i in 0 to 4 loop
        par_sum := par_sum + (c(i + 2) * buf(i));
      end loop;
      
      data_uns <= to_signed(par_sum, bit_width+shif);
--      data_uns <= to_signed(c(1) * to_integer(data_i) + c(2) * buf(0) + c(3) * buf(1) + c(4) * buf(2) + c(5) * buf(3) + c(6) * buf(4), bit_width+shif);
    end if;
  end process process_label;

  
  -- only the bit_width highest bits are sent to the output
  data_o <= data_uns(bit_width+shif-1 downto shif);

end arch;
