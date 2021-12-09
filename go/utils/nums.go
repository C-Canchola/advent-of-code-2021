package utils

func SumNumbers(nums []int) int {
	s := 0
	for _, n := range nums {
		s += n
	}
	return s
}
