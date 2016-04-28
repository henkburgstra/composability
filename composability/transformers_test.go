package composability

import (
	"fmt"
	"testing"
)

func PassTransform(t ITransform) {
	fmt.Println("PassTransform: success")
}

func TestTransformDate(t *testing.T) {
	x := NewTransformDate("22-08-1965")
	PassTransform(x)
}

func TestTransformDateDisplay(t *testing.T) {
	in := []string{"22-08-1965", "1965-08-22"}
	expected := in[0]
	for _, d := range in {
		x := NewTransformDate(d)
		d2 := x.Display()
		if expected != d2 {
			t.Errorf("Display is '%s', expected '%s'", d2, expected)
		}
	}
}

func TestTransformDateStore(t *testing.T) {
	in := []string{"22-08-1965", "1965-08-22"}
	expected := in[1]
	for _, d := range in {
		x := NewTransformDate(d)
		d2 := x.Store()
		if expected != d2 {
			t.Errorf("Display is '%s', expected '%s'", d2, expected)
		}
	}
}
