from datetime import datetime

from lspy.sort import find_sort
from lspy.dig import Inform

def test_sort_by_name():
    informs = []
    for x in range(9, 0, -1):
        inform = Inform(
            name='file{}'.format(x),
            mode=0o100777,
            permission=0o777,
            owner={
                'uid': 0,
                'gid': 0,
                'uname': 'foo',
                'gname': 'bar'
            },
            size=0,
            is_dir=False,
            changed_at=datetime.now(),
            modified_at=datetime.now(),
            accessed_at=datetime.now(),
        )
        informs.append(inform)
    sort_func = find_sort()
    sorted_informs = sort_func[0](informs)
    for x in range(1, 10):
        assert 'file{}'.format(x) == sorted_informs[x - 1].name