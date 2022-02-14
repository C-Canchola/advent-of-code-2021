defmodule Sln do
  def parse_board(s) do

    s
    |> String.split("\n")
    |> Enum.map(&String.split(&1, " "))
    |> Enum.map(&Enum.filter(&1, fn el -> el != "" end))
    |> Enum.map(&Enum.map(&1, fn el -> String.to_integer(el) end))
    |> Enum.map(&List.to_tuple/1)
    |> List.to_tuple()

  end

  defp add_pos_to_tuple(row, col, position_tup_list) do
    [{row, col}] ++ position_tup_list
  end
  defp add_cols(row, position_tup) do
    0..4 |> Enum.reduce(position_tup, fn (el, acc) -> add_pos_to_tuple(row, el, acc) end)
  end
  def get_all_position_tuples() do
    0..4 |> Enum.reduce([], fn (i, acc) -> add_cols(i, acc) end)
  end

  def get_number_at_board_pos(board, {x, y}) do
    board |> elem(x) |> elem(y)
  end

  def board_tuple_to_pos_map(bt) do
    get_all_position_tuples()
    |> Enum.reduce(
      %{},
      fn
        (el, acc) -> Map.put(acc, get_number_at_board_pos(bt, el), el)
      end
    )
  end

  def get_board_possible_score(bt) do
    get_all_position_tuples()
    |> Enum.reduce(
      0,
      fn
        (el, acc) -> acc + get_number_at_board_pos(bt, el)
      end
    )
  end

  def setup_board_for_calcs(bt) do
    %{
      :score => get_board_possible_score(bt),
      :position_map => board_tuple_to_pos_map(bt),
      :count_rows => init_row_or_col_count(),
      :count_cols => init_row_or_col_count(),
      :draws => 0,
      :last_draw => -1
    }
  end
  defp init_row_or_col_count() do
    %{
      0 => 0,
      1 => 0,
      2 => 0,
      3 => 0,
      4 => 0
    }
  end

  defp get_updated_count_row_or_col(board, row_or_col_val, row_or_col) do
    cur_map = board |> Map.fetch!(row_or_col)
    Map.put(cur_map, row_or_col_val, 1 + Map.fetch!(cur_map, row_or_col_val))
  end

  def handle_draw(board, value) do

    if (Map.fetch!(board, :position_map) |> Map.get(value, :not_found)) == :not_found do
      %{
        board |
        draws: Map.fetch!(board, :draws) + 1
      }
    else
      {row, col} = Map.fetch!(board, :position_map) |> Map.fetch!(value)
      %{
        board |
        score: Map.fetch!(board, :score) - value,
        count_rows: get_updated_count_row_or_col(board, row, :count_rows),
        count_cols: get_updated_count_row_or_col(board, col, :count_cols),
        draws: Map.fetch!(board, :draws) + 1,
        last_draw: value
      }
    end
  end

  defp check_rows_or_cols(_, _, []), do: false
  defp check_rows_or_cols(board, row_or_col, remaining) do
    if board |> Map.fetch!(row_or_col) |> Map.fetch!(hd(remaining)) == 5 do
      true
    else
      board |> check_rows_or_cols(row_or_col, tl(remaining))
    end
  end

  defp check_rows_or_cols(board, row_or_col) do
    tries = 0..4 |> Enum.to_list()
    board |> check_rows_or_cols(row_or_col, tries)
  end

  def board_has_won(board) do
    check_rows_or_cols(board, :count_rows) || check_rows_or_cols(board, :count_cols)
  end


  defp do_get_winning_board_score(board, remaining_draws) do
    if board |> board_has_won() do
      %{
        :score => Map.fetch!(board, :score) * Map.fetch!(board, :last_draw),
        :draws => board |> Map.fetch!(:draws),
        :raw_score => board |> Map.fetch!(:score),
        :last_draw => board |> Map.fetch!(:last_draw),
      }
    else
      board
      |> handle_draw(remaining_draws |> hd)
      |> do_get_winning_board_score(remaining_draws |> tl)
    end
  end

  def get_winning_board_score(board, remaining_draws) do
    do_get_winning_board_score(board, remaining_draws)
  end


end

text = IO.read(:stdio, :all)

sections = text
|> String.trim()
|> String.split("\n\n")

moves = hd(sections)
|> String.split(",")
|> Enum.map(&String.to_integer/1)


boards = tl(sections)
|> Enum.map(&Sln.parse_board/1)
|> Enum.map(&Sln.setup_board_for_calcs/1)
|> Enum.map(&Sln.get_winning_board_score(&1, moves))
|> Enum.sort(fn (el1, el2) -> Map.fetch!(el1, :draws) < Map.fetch!(el2, :draws) end)

List.first(boards) |> Map.fetch!(:score) |> IO.inspect()
List.last(boards) |> Map.fetch!(:score) |> IO.inspect()


# test_board = elem(boards, 2) |> Sln.setup_board_for_calcs()
# Sln.get_winning_board_score(test_board, moves) |> IO.inspect()
