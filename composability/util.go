package composability

import (
	"regexp"
	"strings"
)

var (
	reItemKey  = regexp.MustCompile("\\([a-zA-Z0-9-]+\\)")
	rePathInfo = regexp.MustCompile("(.+)(\\()([a-zA-Z0-9-]+)(\\))")
	rePath     = regexp.MustCompile("([\\w-]*)(/|$)(.*)")
)

func Reverse(l []string) []string {
	for i := len(l)/2 - 1; i >= 0; i-- {
		opp := len(l) - 1 - i
		l[i], l[opp] = l[opp], l[i]
	}
	return l
}

type PathInfo struct {
	Field string
	Items []string
	Keys  map[string]string
}

func NewPathInfo(path string) {
	pi := new(PathInfo)
	pi.Items = make([]string, 0, 0)
	pi.Keys = make(map[string]string)

	parts := strings.Split("/")
	tail, parts := parts[len(parts)-1], parts[:len(parts)-1]

	if tail != "" {
		if strings.Contains(tail, "(") {
			pi.Items = append(pi.Items, tail)
		} else {
			pi.Field = tail
		}
	}

}
