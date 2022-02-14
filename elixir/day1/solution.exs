IO.puts("Hello world")
IO.puts("Wow so this is elixir huh?")

defmodule Solution do
  def add_one(x) do
      x + 1
  end

  def filter_sums(l) do
    Enum.at(l, 0) < Enum.at(l, 1)
  end

end

text = IO.read(:stdio, :all)
# numbers = IO.read(:stdio, :all)
#   |> String.trim
#   |> String.split("\n")
#   |> Enum.map(fn n -> String.to_integer(n) end)

text_nums = text
  |> String.trim
  |> String.split("\n")
  |> Enum.map(fn n -> String.to_integer(n) end)


first = text_nums
  |> Enum.chunk_every(1, 1, :discard)
  |> Enum.map(&Enum.sum/1)
  |> Enum.chunk_every(2, 1, :discard)
  |> Enum.filter(&Solution.filter_sums/1)
  |> Enum.count()
  |> IO.inspect

second = text_nums
|> Enum.chunk_every(3, 1, :discard)
|> Enum.map(&Enum.sum/1)
|> Enum.chunk_every(2, 1, :discard)
|> Enum.filter(&Solution.filter_sums/1)
|> Enum.count()
|> IO.inspect
