#!/usr/bin/env python3

''' The simplest web server
    These string resources are the style components
'''

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

a:link, a:visited {
    //color: black;
    text-decoration: none;
    decoration: none;
}

.img_round {
  opacity: 1;
  display: inline;
  height: auto;
  transition: .5s ease;
  backface-visibility: hidden;
  border-radius: 15px;
}

</style>
'''

# EOF