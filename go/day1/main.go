package main

import (
	"advent-of-go/utils"
	"fmt"
	"io"
	"os"
	"strconv"
)

func sliceOfNumbers(r io.Reader) ([]int, error) {
	lines, err := utils.ReadAllLines(r)
	if err != nil {
		return nil, err
	}

	nums := []int{}
	for _, l := range lines {
		num, err := strconv.Atoi(l)
		if err != nil {
			return nil, err
		}
		nums = append(nums, num)
	}
	return nums, nil
}

type counter struct {
	window int
}

func newCounter(window int) *counter {
	return &counter{window: window}
}

type window []int

func (w window) isGreater(other window) bool {
	return utils.SumNumbers(w) > utils.SumNumbers(other)
}

func (c *counter) getIncreaseCount(nums []int) int {
	count := 0

	for i := 0; i < len(nums)-c.window+1; i++ {
		first, second := nums[i:i+c.window], nums[i+1:i+c.window+1]
		if !window(second).isGreater(window(first)) {
			continue
		}
		count++
	}
	return count
}

func main() {

	nums, err := sliceOfNumbers(os.Stdin)
	if err != nil {
		panic(err)
	}

	singleCounter := newCounter(1)
	fmt.Println(singleCounter.getIncreaseCount(nums))

	threeCounter := newCounter(3)
	fmt.Println(threeCounter.getIncreaseCount(nums))
}
