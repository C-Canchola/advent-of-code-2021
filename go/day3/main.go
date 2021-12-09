package main

import (
	"advent-of-go/utils"
	"fmt"
	"log"
	"os"
	"strconv"
)

type counter struct {
	length     int
	zeroCounts []int
	oneCounts  []int
}

func newCounter(lines []string) counter {
	length := len(lines[0])
	zeroes, ones := make([]int, length), make([]int, length)

	for _, l := range lines {
		for idx, c := range l {
			switch c {
			case '0':
				zeroes[idx] += 1
			case '1':
				ones[idx] += 1
			}
		}
	}
	return counter{length: length, zeroCounts: zeroes, oneCounts: ones}
}

func (c counter) gammaRate() string {
	rate := ""
	for idx := range c.oneCounts {
		if c.zeroCounts[idx] > c.oneCounts[idx] {
			rate += "0"
			continue
		}
		rate += "1"
	}
	return rate
}

func gammaToEpsilon(gamma string) string {
	rate := ""
	for _, c := range gamma {
		if c == '0' {
			rate += "1"
			continue
		}
		rate += "0"
	}
	return rate
}

type powerConsumptionRates struct {
	gamma, epsilon string
}

func (c counter) powerConsumptionRates() powerConsumptionRates {
	gamma := c.gammaRate()
	return powerConsumptionRates{gamma: gamma, epsilon: gammaToEpsilon(gamma)}
}

func multTwoBinaryStrings(s1, s2 string) (int, error) {
	v1, err := strconv.ParseInt(s1, 2, 64)
	if err != nil {
		return 0, err
	}
	v2, err := strconv.ParseInt(s2, 2, 64)
	if err != nil {
		return 0, err
	}
	return int(v2 * v1), nil
}


func (c counter) powerConsumption() (int, error) {
	rates := c.powerConsumptionRates()

	gammaVal, err := strconv.ParseInt(rates.gamma, 2, 64)
	if err != nil {
		return 0, err
	}

	epsilonVal, err := strconv.ParseInt(rates.epsilon, 2, 64)
	if err != nil {
		return 0, err
	}
	return int(epsilonVal * gammaVal), nil
}

func main() {
	lines, err := utils.ReadAllLinesTrimmed(os.Stdin)
	if err != nil {
		log.Fatal(err)
	}
	counter := newCounter(lines)
	pc, err := counter.powerConsumption()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(pc)
}
