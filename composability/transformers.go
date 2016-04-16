package composability

import (
	"regexp"
)

//interface ITransformer {
//	func Display() string;
//	func Store() string;
//}

type TransformDisplay func() string
type TransformStore func() string

var (
	reDdmmyyyy = regexp.MustCompile(`(\d{1,2})(-|/)(\d{1,2})(-|/)(\d{4})`)
	reYyyymmdd = regexp.MustCompile("(\\d{4})(-|/)(\\d{1,2})(-|/)(\\d{1,2})")
)

type Transform struct {
	Attributes map[string]*Attribute
	Display    TransformDisplay
	Store      TransformStore
}

func NewTransform(kwargs map[string]*Attribute) *Transform {
	t := new(Transform)
	t.Attributes = kwargs
	t.Display = func() string {
		if v, ok := t.Attributes["value"]; ok {
			return v.String()
		} else {
			return ""
		}
	}
	t.Store = func() string {
		return t.Display()
	}
	return t
}

func NewTransformDate(kwargs map[string]*Attribute) *Transform {
	t := NewTransform(kwargs)
	return t
}
