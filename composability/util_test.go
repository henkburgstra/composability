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

//    def test_path_info(self):
//        p = PathInfo("this(1)/is(2)/a(3)/path(4)/name")
//        self.assertEqual(p.field, "name")
//        self.assertEqual(len(p.items), 4)
//        self.assertEqual(p.keys["is"], "2")

func TestPathInfo(t *testing.T) {
	p := NewPathInfo("this(1)/is(2)/a(3)/path(4)/name")
	if p.Field != "name" {
		t.Error("expected 'name', got ", p.Field)
	}
}
