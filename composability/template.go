package composability

import (
	"encoding/json"
	"fmt"
	"strconv"
	"strings"
)

type Display string
type Orientation string
type Position string

const (
	DISP_GROUP  Display = "GROUP"
	DISP_INLINE Display = "INLINE"
	DISP_UNDER  Display = "UNDER"
	DISP_RIGHT  Display = "RIGHT"

	ORI_HORIZONTAL Orientation = "HORIZONTAL"
	ORI_VERTICAL   Orientation = "VERTICAL"

	POS_ABOVE  Position = "ABOVE"
	POS_LEFT   Position = "LEFT"
	POS_BEFORE Position = "BEFORE"
	POS_AFTER  Position = "AFTER"
)

func StrToInt(s string) int64 {
	if v, err := strconv.ParseInt(s, 0, 64); err == nil {
		return v
	}
	return 0
}

type Attrs map[string]*Attribute

func (al Attrs) ToString(name string) string {
	if attr, ok := al[name]; ok {
		return attr.String()
	}
	return ""
}

func (al Attrs) ToInt(name string) int64 {
	if attr, ok := al[name]; ok {
		return attr.Int()
	}
	return 0
}

type Attribute struct {
	value interface{}
}

func Attr(value interface{}) *Attribute {
	a := new(Attribute)
	a.value = value
	return a
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

func (a *Attribute) Value() interface{} {
	return a.value
}

func (a *Attribute) UnmarshalJSON(b []byte) (err error) {
	err = json.Unmarshal(b, &a.value)
	return
}

func (a *Attribute) SetDefault(name string) interface{} {
	switch name {
	case "background_colour":
		a.value = "white"
	case "colcount":
		a.value = 1
	case "colspan":
		a.value = 1
	case "rowspan":
		a.value = 1
	case "orientation":
		a.value = ORI_HORIZONTAL
	case "display":
		a.value = DISP_INLINE
	case "label_position":
		a.value = POS_ABOVE
	}
	return a.value
}

type Template struct {
	Parent     *Template
	Kind       string                `json:"kind"`
	Name       string                `json:"name"`
	Title      string                `json:"title"`
	Value      interface{}           `json:"value"`
	Readonly   bool                  `json:"readonly"`
	Visible    bool                  `json:"visible"`
	Include    string                `json:"include"`
	Attributes map[string]*Attribute `json:"attributes"`
	Items      []*Template
	items_map  map[string]*Template
}

func NewTemplate(kind string) *Template {
	t := new(Template)
	t.Kind = kind
	t.Attributes = make(map[string]*Attribute)
	t.Items = make([]*Template, 0, 0)
	t.items_map = make(map[string]*Template)
	return t
}

func (t *Template) Attr(name string) *Attribute {
	var attr *Attribute
	if _, ok := t.Attributes[name]; ok {
		attr = t.Attributes[name]
	} else {
		attr = new(Attribute)
		attr.SetDefault(name)
	}
	return attr
}

func (t *Template) SetAttr(name string, value interface{}) {
	attr := new(Attribute)
	attr.value = value
}

func (t *Template) Add(template *Template) {
	if template.Attr("background_colour").String() == "" {
		template.SetAttr("background_colour", t.Attr("background_colour").String())
	}
	template.Parent = t
	t.Items = append(t.Items, template)
	t.items_map[template.Name] = template
}

func (t *Template) Insert(siblingName string, pos Position, template *Template) {
	items := t.Items
	t.Items = make([]*Template, 0, 0)
	t.items_map = make(map[string]*Template)

	for _, item := range items {
		if item.Name == siblingName {
			if pos == POS_BEFORE {
				t.Add(template)
				t.Add(item)
			} else {
				t.Add(item)
				t.Add(template)
			}
		} else {
			t.Add(item)
		}
	}
}

func (t *Template) Delete(template *Template) {
	if _, ok := t.items_map[template.Name]; ok {
		delete(t.items_map, template.Name)
		index := -1
		for i, item := range t.Items {
			if item.Name == template.Name {
				index = i
				break
			}
		}
		if index != -1 {
			t.Items = append(t.Items[:index], t.Items[index+1:]...)
		}
	}
}

func (t *Template) Clear() {
	t.Items = make([]*Template, 0, 0)
	t.items_map = make(map[string]*Template)
}

func (t *Template) Get(name string) *Template {
	return t.items_map[name]
}

func (t *Template) GetParentName() string {
	if t.Parent != nil {
		return t.Parent.Name
	}
	if t.Name == "" {
		return ""
	}
	return strings.Join(strings.Split(t.Name, "/"), "/")
}
