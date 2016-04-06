package composability

import (
	"encoding/json"
	"fmt"
	"strconv"
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

func (t *Template) Attr(name string) *Attribute {
	var attr *Attribute
	if attr, ok := t.Attributes[name]; !ok {
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

//    def insert(self, sibling_name, pos, template):
//        items = self.items
//        self.items = []
//        self.items_dict = {}
//        for item in items:
//            if item.name == sibling_name:
//                if pos == self.POS_BEFORE:
//                    self.add(template)
//                    self.add(item)
//                else:
//                    self.add(item)
//                    self.add(template)
//            else:
//                self.add(item)

func (t *Template) Insert(siblingName string, pos Position, template *Template) {
	items := t.items
	t.items = make([]*Template, 0, 0)
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
