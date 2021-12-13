

library ieee;
  use ieee.std_logic_1164.all;
  use ieee.numeric_std.all;


entity heartbeat is
  generic (
    low_bit  : natural := 23;
    high_bit : natural := 27
  );
  port (
    clk: in std_logic;
    led: out std_logic_vector(high_bit - low_bit downto 0)
  );
end heartbeat;


-----------------------------------------------------------------------

architecture rtl of heartbeat is

  signal counter: unsigned(31 downto 0);	
	
begin
	
  process(clk) begin

    if rising_edge(clk) then

      counter <= counter + 1;

    end if;

  end process;

  led <= std_logic_vector(counter(high_bit downto low_bit));

end architecture rtl;
