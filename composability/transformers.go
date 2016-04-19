package composability

import (
	"fmt"
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
		match := reYyyymmdd.FindStringSubmatch(t.Attributes.ToString("value"))
		if match != nil {
			y, _ = strconv.ParseInt(match[1], 10, 64)
			m, _ = strconv.ParseInt(match[3], 10, 64)
			d, _ = strconv.ParseInt(match[5], 10, 64)
			t.Attributes["_y"] = NewAttribute(y)
			t.Attributes["_m"] = NewAttribute(m)
			t.Attributes["_d"] = NewAttribute(d)

		} else {
			match = reDdmmyyyy.FindStringSubmatch(t.Attributes.ToString("value"))
			if match != nil {
				y, _ = strconv.ParseInt(match[1], 10, 64)
				m, _ = strconv.ParseInt(match[3], 10, 64)
				d, _ = strconv.ParseInt(match[5], 10, 64)
				t.Attributes["_y"] = NewAttribute(y)
				t.Attributes["_m"] = NewAttribute(m)
				t.Attributes["_d"] = NewAttribute(d)
			}
		}
	}
	t.Display = func() string {
		return fmt.Sprintf("%02d-%02d-%04d",
			t.Attributes.ToInt("_d"),
			t.Attributes.ToInt("_m"),
			t.Attributes.ToInt("_y"))
	}
	t.Store = func() string {
		return fmt.Sprintf("%04d-%02d-%02d",
			t.Attributes.ToInt("_y"),
			t.Attributes.ToInt("_m"),
			t.Attributes.ToInt("_d"))
	}
	return t
}
