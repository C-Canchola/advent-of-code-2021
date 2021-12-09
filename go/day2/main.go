package main

import (
	"advent-of-go/utils"
	"errors"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

type move struct {
	direction string
	amount    int
}

var validDirections = map[string]bool{
	"forward": true,
	"up":      true,
	"down":    true,
}

func convertLineToMove(l string) (move, error) {
	splt := strings.Split(l, " ")
	dir, amount := strings.TrimSpace(splt[0]), strings.TrimSpace(splt[1])
	if !validDirections[dir] {
		return move{}, errors.New("invalid direction: " + dir)
	}
	amountNum, err := strconv.Atoi(amount)
	if err != nil {
		return move{}, err
	}
	return move{direction: dir, amount: amountNum}, nil
}

func convertLinesToMoves(lines []string) ([]move, error) {
	moves := make([]move, 0, len(lines))
	for _, l := range lines {
		move, err := convertLineToMove(l)
		if err != nil {
			return nil, err
		}
		moves = append(moves, move)
	}
	return moves, nil
}

func distanceNoAim(moves []move) int {
	horizontal, depth := 0, 0

	for _, m := range moves {
		switch m.direction {
		case "forward":
			horizontal += m.amount
		case "up":
			depth -= m.amount
		case "down":
			depth += m.amount
		}
	}
	return horizontal * depth
}

func distanceWithAim(moves []move) int {
	horizontal, depth, aim := 0, 0, 0

	for _, m := range moves {
		switch m.direction {
		case "forward":
			horizontal += m.amount
			depth += m.amount * aim
		case "up":
			aim -= m.amount
		case "down":
			aim += m.amount
		}
	}

	return horizontal * depth
}

func main() {
	lines, err := utils.ReadAllLines(os.Stdin)
	if err != nil {
		log.Fatal(err)
	}
	moves, err := convertLinesToMoves(lines)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(distanceNoAim(moves))
	fmt.Println(distanceWithAim(moves))
}
