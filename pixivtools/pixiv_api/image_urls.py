from typing import NamedTuple, Callable


class _ArtworkUrl:
    def __init__(self, _template: str, i: int):
        self._template = _template
        self._idx = i

    @property
    def original(self): # 原图
        return self._template['original'].format(self._idx)
    
    @property
    def regular(self):  # 一般(一般是1200*1200) https://i.pximg.net/img-master/img/
        return self._template['regular'].format(self._idx)
    
    @property
    def small(self):    # 小图(一般是540*540) https://i.pximg.net/c/48x48/custom-thumb/img/...
        return self._template['small'].format(self._idx)
    
    @property
    def thumb(self):    # 缩略图(一般250*250) https://i.pximg.net/c/250x250_80_a2/custom-thumb/img/...
        return self._template['thumb'].format(self._idx)
    
    @property
    def mini(self):     # 迷你图(一般48*48) https://i.pximg.net/c/48x48/custom-thumb/img/...
        return self._template['mini'].format(self._idx)

    def __str__(self):
        return f"original: {self.original}, regular: {self.regular}, small: {self.small}, thumb: {self.thumb}, mini: {self.mini}"


key2transfunc = {
    'original': lambda x: '_p{}.'.join(x.split('_p0.')),
    'regular': lambda x: '_p{}_'.join(x.split('_p0_')),
    'small': lambda x: '_p{}_'.join(x.split('_p0_')),
    'thumb': lambda x: '_p{}_'.join(x.split('_p0_')),
    'mini': lambda x: '_p{}_'.join(x.split('_p0_')),
}


def _load_artwork_url_gen(urls) -> Callable[[int], _ArtworkUrl]:
    inject = {}
    for k, v in urls.items():
        inject[k] = key2transfunc[k](v)
    def gen_url(idx):
        return _ArtworkUrl(inject, idx)
    return gen_url
