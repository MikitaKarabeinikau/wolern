import pytest

import fetchers


def test_hide_similar_parts():
    assert fetchers.hide_similar_parts('vocal','vocalism') == '.....ism'
    assert fetchers.hide_similar_parts('break','briak') == 'briak'
    assert fetchers.hide_similar_parts('to','to') == 'to'

def test_None_argument_in_hide_similar_parts():
    with pytest.raises(ValueError,match = 'Could compare with None argument'):
        assert fetchers.hide_similar_parts(None,None)
        assert fetchers.hide_similar_parts(None,"make")
        assert fetchers.hide_similar_parts('done',None)

def test_not_string_arguments_in_hide_similar_parts():
    with pytest.raises(ValueError,match='Values should be string type'):
        assert fetchers.hide_similar_parts([],1)
        assert fetchers.hide_similar_parts({},"make")
        assert fetchers.hide_similar_parts('done',set([1,3,4,5]))


