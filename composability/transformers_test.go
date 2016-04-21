package composability

import (
	"fmt"
	"testing"
)

func PassTransform(t *Transform) {
	fmt.Printf("success")
}

func TestTransformDate(t *testing.T) {
	x := NewTransformDate(Attrs{"y": Attr(1965), "m": Attr(8), "d": Attr(22)})
	PassTransform((*Transform)(x))
}
