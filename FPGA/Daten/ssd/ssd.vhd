-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file ssd.vhd
--! @brief displays a four digit number on four seven segment displays (ssd)
--! @author: Philipp Horn <philipp.horn@cern.ch>
--! @details: This module continues to divide the input data by ten and outputs
--!           the remainder to the individual displays
--------------------------------------------------------------------------------

library IEEE;
use     IEEE.std_logic_1164.ALL;
use     IEEE.numeric_std.ALL;

entity ssd is
  generic (
    -- signals, which are declared here can be used in the port definition
    bit_width : positive := 14;
    -- generic is passed to higher module
    invert : boolean := true
  );
  port (
    clk : in  std_logic;

    data_i : in  signed(bit_width-1 downto 0);

    ss_d1_o : out std_logic_vector(6 downto 0);
    ss_d2_o : out std_logic_vector(6 downto 0);
    ss_d3_o : out std_logic_vector(6 downto 0);
    ss_d4_o : out std_logic_vector(6 downto 0)
  );
end entity;

architecture arch of ssd is

  -- number of seven segment displays
  constant N_ssd : positive := 4;

  -- type definition: array of std_logic_vectors
  type ssd_t is array (natural range <>) of std_logic_vector(6 downto 0);
  -- ss_ds is an array of std_logic_vectors with length N_ssd
  signal ss_ds : ssd_t (N_ssd-1 downto 0);

  type num_arr is array (natural range <>) of signed(4 downto 0);
  -- matrix, which contains the quotient of each division step
  signal quotient : num_arr (3 downto 0);
  -- matrix, which contains the remainder of each division step
--  signal remainder:


begin
  
  generate_label: for i in 3 downto 0 generate
    
    quotient(i) <= to_signed(((to_integer(data_i) / 10**i) mod 10), 5);
    
    map_label: entity work.single_disp
    generic map(
    invert => true
    )
    port map(
    number_i => quotient(i),
    seg_o => ss_ds(i)
    );
  end generate;

  -- connect the single elements of the ss_ds with the output displays
  ss_d1_o <= ss_ds(0);
  ss_d2_o <= ss_ds(1);
  ss_d3_o <= ss_ds(2);
  ss_d4_o <= ss_ds(3);

end arch;
