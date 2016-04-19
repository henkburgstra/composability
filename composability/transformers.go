package composability

import (
	"regexp"
	"strconv"
)

//interface ITransformer {
//	func Display() string;
//	func Store() string;
//}

type TransformDisplay func() string
type TransformStore func() string

var (
	reDdmmyyyy = regexp.MustCompile(`(\d{1,2})(-|/)(\d{1,2})(-|/)(\d{4})`)
	reYyyymmdd = regexp.MustCompile(`(\d{4})(-|/)(\d{1,2})(-|/)(\d{1,2})`)
)

type Transform struct {
	Attributes AttributeList
	Display    TransformDisplay
	Store      TransformStore
}

func NewTransform(kwargs AttributeList) *Transform {
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
	y := t.Attributes.ToInt("_y")
	m := t.Attributes.ToInt("_m")
	d := t.Attributes.ToInt("_d")
	if y == 0 || m == 0 || d == 0 {
		m := reYyyymmdd.FindStringSubmatch(t.Attributes.ToString("value"))
		if m != nil {
			t.Attributes["_y"], _ = NewAttribute(strconv.Atoi(m[1]))
			t.Attributes["_m"], _ = NewAttribute(strconv.Atoi(m[3]))
			t.Attributes["_d"], _ = NewAttribute(strconv.Atoi(m[5]))
		}
	}
	t.Display = func() string {
		return ""
	}
	t.Store = func() string {
		return ""
	}
	return t
}
