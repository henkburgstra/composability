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
	Attributes Attrs
	Display    TransformDisplay
	Store      TransformStore
}

func NewTransform(kwargs Attrs) *Transform {
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

type TransformDate Transform

func NewTransformDate(kwargs map[string]*Attribute) *TransformDate {
	t := (*TransformDate)(NewTransform(kwargs))
	y := int(t.Attributes.ToInt("y"))
	m := int(t.Attributes.ToInt("m"))
	d := int(t.Attributes.ToInt("d"))
	if y == 0 || m == 0 || d == 0 {
		match := reYyyymmdd.FindStringSubmatch(t.Attributes.ToString("value"))
		if match != nil {
			y, _ = strconv.Atoi(match[1])
			m, _ = strconv.Atoi(match[3])
			d, _ = strconv.Atoi(match[5])
			t.Attributes["y"] = Attr(y)
			t.Attributes["m"] = Attr(m)
			t.Attributes["d"] = Attr(d)

		} else {
			match = reDdmmyyyy.FindStringSubmatch(t.Attributes.ToString("value"))
			if match != nil {
				y, _ = strconv.Atoi(match[1])
				m, _ = strconv.Atoi(match[3])
				d, _ = strconv.Atoi(match[5])
				t.Attributes["y"] = Attr(y)
				t.Attributes["m"] = Attr(m)
				t.Attributes["d"] = Attr(d)
			}
		}
	}
	t.Display = func() string {
		return fmt.Sprintf("%02d-%02d-%04d",
			t.Attributes.ToInt("d"),
			t.Attributes.ToInt("m"),
			t.Attributes.ToInt("y"))
	}
	t.Store = func() string {
		return fmt.Sprintf("%04d-%02d-%02d",
			t.Attributes.ToInt("y"),
			t.Attributes.ToInt("m"),
			t.Attributes.ToInt("d"))
	}
	return t
}

func (t *TransformDate) d() int {
	return int(t.Attributes.ToInt("d"))
}

func (t *TransformDate) m() int {
	return int(t.Attributes.ToInt("m"))
}

func (t *TransformDate) y() int {
	return int(t.Attributes.ToInt("y"))
}
