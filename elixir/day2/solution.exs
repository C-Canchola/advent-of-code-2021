
defmodule Solution do

  def convert(line) do
    splt = String.split(line, " ")
    [direction, amount] = splt
    {direction, String.to_integer(amount)}
  end

  def accum({"forward", amt }, {v, h}), do: {v, h + amt}
  def accum({"down", amt}, {v, h}), do: {v + amt, h}
  def accum({"up", amt}, {v, h}), do: {v - amt, h}

  def accum({"forward", amt}, {v, h, a}), do: {v + a * amt, h + amt, a}
  def accum({"down", amt}, {v, h, a}), do: {v, h, a + amt}
  def accum({"up", amt}, {v, h, a}), do: {v, h, a - amt}

  def calc({v, h}), do: v * h
  def calc({v, h, _}), do: v * h

  def solve(lines, tup) do
    lines
    |> Enum.map(&convert/1)
    |> Enum.reduce(tup, &accum/2)
    |> calc
    |> IO.inspect
  end

end

text = IO.read(:stdio, :all)


lines = text
  |> String.trim
  |> String.split("\n")


Solution.solve(lines, {0, 0})
Solution.solve(lines, {0, 0, 0})
