package utils

import (
	"bufio"
	"io"
	"strings"
)

// ReadAllLines returns all the lines as an array of strings from a given reader
func ReadAllLines(r io.Reader) ([]string, error) {
	s := bufio.NewScanner(r)
	lines := []string{}
	for s.Scan() {
		lines = append(lines, s.Text())
	}
	if s.Err() != nil {
		return nil, s.Err()
	}
	return lines, nil
}

func ReadAllLinesTrimmed(r io.Reader) ([]string, error) {
	lines, err := ReadAllLines(r)
	if err != nil {
		return nil, err
	}
	trimLines := make([]string, 0, len(lines))
	for _, l := range lines {
		trimLines = append(trimLines, strings.TrimSpace(l))
	}
	return trimLines, nil
}
