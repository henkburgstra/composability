package composability

import (
	"fmt"
	"regexp"
	"strconv"
)

type ITransform interface {
	Display() string
	Store() string
	Value() interface{}
}

var (
	reDdmmyyyy = regexp.MustCompile(`(\d{1,2})(-|/)(\d{1,2})(-|/)(\d{4})`)
	reYyyymmdd = regexp.MustCompile(`(\d{4})(-|/)(\d{1,2})(-|/)(\d{1,2})`)
)

type Transform Attribute

func NewTransform(value interface{}) *Transform {
	t := (*Transform)(Attr(value))
	return t
}

func (t *Transform) Display() string {
	return (*Attribute)(t).String()
}

func (t *Transform) Store() string {
	return t.Display()
}

func (t *Transform) Value() interface{} {
	return (*Attribute)(t).Value()
}

type TransformDate struct {
	*Transform
	y, m, d int
}

func NewTransformDate(value interface{}) *TransformDate {
	t := new(TransformDate)
	t.Transform = NewTransform(value)
	match := reYyyymmdd.FindStringSubmatch((*Attribute)(t.Transform).String())
	if match != nil {
		t.y, _ = strconv.Atoi(match[1])
		t.m, _ = strconv.Atoi(match[3])
		t.d, _ = strconv.Atoi(match[5])

	} else {
		match = reDdmmyyyy.FindStringSubmatch((*Attribute)(t.Transform).String())
		if match != nil {
			t.y, _ = strconv.Atoi(match[5])
			t.m, _ = strconv.Atoi(match[3])
			t.d, _ = strconv.Atoi(match[1])
		}
	}
	return t
}

func (t *TransformDate) Display() string {
	return fmt.Sprintf("%02d-%02d-%04d", t.d, t.m, t.y)
}

func (t *TransformDate) Store() string {
	return fmt.Sprintf("%04d-%02d-%02d", t.y, t.m, t.d)
}

func (t *TransformDate) D() int {
	return t.d
}

func (t *TransformDate) M() int {
	return t.m
}

func (t *TransformDate) Y() int {
	return t.y
}
