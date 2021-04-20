#!/usr/bin/env python3

''' The simplest web server '''

# These string resources are the style components

mystyle = '''
<style>
.container {
  position: relative;
  width: 50%;
}
.image {
  opacity: 1;
  display: inline;
  height: auto;
  transition: .5s ease;
  backface-visibility: hidden;
}
.container {
  position: relative;
  width: 50%;
}
.container:hover .image {
  opacity: 0.3;
}
.container:hover .middle {
  opacity: 1;
}

</style>
'''

# EOF