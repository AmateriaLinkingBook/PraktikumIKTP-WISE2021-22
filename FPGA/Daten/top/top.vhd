-- EMACS settings: -*-  tab-width: 2; indent-tabs-mode: nil -*-
-- vim: tabstop=2:shiftwidth=2:expandtab
-- kate: tab-width 2; replace-tabs on; indent-width 2;
--------------------------------------------------------------------------------
--! @file top.vhd
--! @brief top module
--! @author: Philipp Horn <philipp.horn@cern.ch>
--------------------------------------------------------------------------------

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity top is
  generic (
    OFFSET      : positive := 1024;
    CTRL_BIT    : natural  := 1;
    UART_DBIT   : positive := 8;    -- uart data bits in uart communication
    SAMPLES_MAX : positive := 32;
    SIMULATE    : boolean  := true;
    bit_width   : positive := 14;
    invert      : boolean  := true
  );
  port (
    clk : in std_logic;

    button_i  : in std_logic;
    btn_rst   : in std_logic;

    led_o : out std_logic_vector(1 downto 0) := (others => '0');

    ss_d1_o : out std_logic_vector(6 downto 0) := (others => '0');
    ss_d2_o : out std_logic_vector(6 downto 0) := (others => '0');
    ss_d3_o : out std_logic_vector(6 downto 0) := (others => '0');
    ss_d4_o : out std_logic_vector(6 downto 0) := (others => '0');

    uart_rxd_i : in std_logic;          -- receive data
    uart_txd_o : out std_logic          -- transmit data
  );
end top;

----------------------------------------------------------------------

architecture arch of top is

  signal start    : std_logic := '0';
  signal data_raw : signed(bit_width-1 downto 0) := (others => '0');
  signal data_filtered : signed(bit_width-1 downto 0) := (others => '0');
  signal data_max : signed(bit_width-1 downto 0);


begin

  injector_inst : entity work.injector
  generic map (
    OFFSET      => OFFSET,
    BIT_WIDTH   => 2 * (UART_DBIT - CTRL_BIT),
    SAMPLES_MAX => SAMPLES_MAX,
    UART_DBIT   => UART_DBIT,
    SIMULATE    => SIMULATE
  )
  port map (
    clk_50  => clk,
    btn_rst => btn_rst,

    -- serial uart signal lines
    rx     => uart_rxd_i,
    tx     => uart_txd_o,

    start  => start,
    leds   => led_o,

    -- data output with associated data valid
    data_valid => open,
    data_out   => data_raw
  );
  
  lohi_detect_inst : entity work.lohi_detect
  port map (
    clk => clk,
    sig_i => button_i,
    sig_o => start
  );
  
  filter_inst : entity work.filter
  generic map(
    bit_width => bit_width
  )
  port map (
    clk => clk,
    data_i => data_raw,
    data_o => data_filtered
  );
  
  max_find_inst : entity work.max_find
  generic map(
    bit_width => bit_width
  )
  port map (
    clk => clk,
    start_i => start,
    data_i => data_filtered,
    data_o => data_max
  );
  
  ssd_inst : entity work.ssd
  generic map(
    bit_width => bit_width,
    invert => invert
  )
  port map(
    clk => clk,
    data_i => data_max,

    ss_d1_o => ss_d1_o,
    ss_d2_o => ss_d2_o,
    ss_d3_o => ss_d3_o,
    ss_d4_o => ss_d4_o
  );

end arch;
