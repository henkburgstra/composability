package composability

import (
	"testing"
)

func TestStripKey(t *testing.T) {
	for _, p := range []string{"path(1)/with(2)/keys", "path(a)/with(b)/keys", "path(a-1)/with(b-2)/keys"} {
		if StripKey(p) != "path/with/keys" {
			t.Error(StripKey(p), " != ", "path/with/keys")
		}
	}
}

func TestPathInfo(t *testing.T) {
	p := NewPathInfo("this(1)/is(2)/a(3)/path(4)/name")
	if p.Field != "name" {
		t.Error("expected 'name', got ", p.Field)
	}
	if len(p.Items) != 4 {
		t.Error("PathInfo instance has ", len(p.Items), ", expected 4.")
	}
	if p.Keys["is"] != "2" {
		t.Error("PathInfo key 'is' equals ", p.Keys["is"], ", expected '2'.")
	}
}
