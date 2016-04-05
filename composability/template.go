package composability

import (
	"encoding/json"
	"fmt"
	"strconv"
)

const (
	DISP_GROUP  = "GROUP"
	DISP_INLINE = "INLINE"
	DISP_UNDER  = "UNDER"
	DISP_RIGHT  = "RIGHT"

	ORI_HORIZONTAL = "HORIZONTAL"
	ORI_VERTICAL   = "VERTICAL"

	POS_ABOVE  = "ABOVE"
	POS_LEFT   = "LEFT"
	POS_BEFORE = "BEFORE"
	POS_AFTER  = "AFTER"
)

func StrToInt(s string) int64 {
	if v, err := strconv.ParseInt(s, 0, 64); err == nil {
		return v
	}
	return 0
}

type Attribute struct {
	value interface{}
}

func (a *Attribute) Int() int64 {
	switch value := a.value.(type) {
	case int:
		return int64(value)
	case int8:
		return int64(value)
	case int16:
		return int64(value)
	case int32:
		return int64(value)
	case int64:
		return value
	case *int:
		return int64(*value)
	case *int8:
		return int64(*value)
	case *int16:
		return int64(*value)
	case *int32:
		return int64(*value)
	case *int64:
		return *value
	case string:
		return StrToInt(value)
	case *string:
		return StrToInt(*value)
	case []byte:
		return StrToInt(string(value))
	case *[]byte:
		return StrToInt(string(*value))
	}
	return 0
}

func (a *Attribute) String() string {
	switch value := a.value.(type) {
	case int, int8, int16, int32, int64:
		return fmt.Sprintf("%d", value)
	case *int:
		return fmt.Sprintf("%d", *value)
	case *int8:
		return fmt.Sprintf("%d", *value)
	case *int16:
		return fmt.Sprintf("%d", *value)
	case *int32:
		return fmt.Sprintf("%d", *value)
	case *int64:
		return fmt.Sprintf("%d", *value)
	case string:
		return value
	case *string:
		return *value
	case []byte:
		return string(value)
	case *[]byte:
		return string(*value)
	case nil:
		return "NULL"
	}
	return ""
}

func (a *Attribute) UnmarshalJSON(b []byte) (err error) {
	err = json.Unmarshal(b, a.value)
	return
}

func (a *Attribute) Default(name string) interface{} {
	switch name {
	case "background_colour":
		return "white"
	case "colcount":
		return 1
	case "colspan":
		return 1
	case "rowspan":
		return 1
	case "orientation":
		return ORI_HORIZONTAL
	case "display":
		return DISP_INLINE
	case "label_position":
		return POS_ABOVE
	}
	return nil
}

type Template struct {
	Kind       string                `json:"kind"`
	Name       string                `json:"name"`
	Title      string                `json:"title"`
	Value      interface{}           `json:"value"`
	Readonly   bool                  `json:"readonly"`
	Visible    bool                  `json:"visible"`
	Attributes map[string]*Attribute `json:"attributes"`
	Items      []*Template
	items_map  map[string]*Template
}

func NewTemplate(kind string) *Template {
	t := new(Template)
	t.Kind = kind
	t.Items = make([]*Template, 0, 0)
	t.items_map = make(map[string]*Template)
	return t
}
