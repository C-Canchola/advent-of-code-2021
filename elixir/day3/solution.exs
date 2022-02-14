text = IO.read(:stdio, :all)


lines = text
  |> String.trim
  |> String.split("\n")


defmodule Sln do
  def create_mapper(lines), do: fn pos -> lines |> Enum.map(&String.at(&1, pos)) end

  def char_count_accum("0", {zero_count, one_count}), do: {zero_count + 1, one_count}
  def char_count_accum("1", {zero_count, one_count}), do: {zero_count, one_count + 1}

  def turn_to_char_counts(pos_chars), do: pos_chars |> Enum.reduce({0, 0}, &char_count_accum/2)
  def turn_to_char_counts(lines, pos) do
    lines
    |> Enum.map(&String.at(&1, pos))
    |> turn_to_char_counts()
  end
  def char_counts_to_bit({zero_count, one_count}) when zero_count > one_count, do: "0"
  def char_counts_to_bit({zero_count, one_count}) when one_count > zero_count, do: "1"

  def parse_binary(b) do
    {num, _} = Integer.parse(b, 2)
    num
  end

  def gamma_rate_bit_to_epsilon("0"), do: "1"
  def gamma_rate_bit_to_epsilon("1"), do: "0"

  def bits_to_num(bs), do: Enum.join(bs) |> parse_binary()

  def bit_count(lines), do: String.length(hd(lines))
  def range_end(lines), do: bit_count(lines) - 1

  defp filter_oxygen({zero_count, one_count}, pos) when zero_count > one_count, do: fn l -> String.at(l, pos) == "0" end
  defp filter_oxygen({_, _}, pos), do: fn l -> String.at(l, pos) == "1" end

  defp filter_co2({zero_count, one_count}, pos) when zero_count > one_count, do: fn l -> String.at(l, pos) == "1" end
  defp filter_co2({_, _}, pos), do: fn l-> String.at(l, pos) == "0" end

  defp oxygen_rating([rating], _), do: rating
  defp oxygen_rating(lines, pos) do
    char_counts = turn_to_char_counts(lines, pos)
    filtered_lines = lines |> Enum.filter(filter_oxygen(char_counts, pos))

    oxygen_rating(filtered_lines, pos + 1)
  end

  def oxygen_rating(lines) do
    oxygen_rating(lines, 0)
  end

  defp co2_rating([rating], _), do: rating
  defp co2_rating(lines, pos) do
    char_counts = turn_to_char_counts(lines, pos)
    filtered_lines = lines |> Enum.filter(filter_co2(char_counts, pos))

    co2_rating(filtered_lines, pos + 1)
  end

  def co2_rating(lines) do
    co2_rating(lines, 0)
  end

end

positions = 0..Sln.range_end(lines)
|> Enum.map(&(&1))


positional_chars = positions
|> Enum.map(Sln.create_mapper(lines))

char_counts = positional_chars |> Enum.map(&Sln.turn_to_char_counts/1)

gamma_rate_bits = char_counts |> Enum.map(&Sln.char_counts_to_bit/1)
epsilon_rate_bits = gamma_rate_bits |> Enum.map(&Sln.gamma_rate_bit_to_epsilon/1)

answer_1 = Sln.bits_to_num(gamma_rate_bits) * Sln.bits_to_num(epsilon_rate_bits)
answer_1 |> IO.inspect()

answer_2 = (lines |> Sln.oxygen_rating |> Sln.parse_binary) * (lines |> Sln.co2_rating |> Sln.parse_binary)
answer_2 |> IO.inspect()
