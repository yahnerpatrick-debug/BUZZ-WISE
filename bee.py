"""The BUZZ-CHECK bee."""


def bee_svg(uid, css_class='bee'):
    """Return the bee as SVG. `uid` keeps ids unique when two bees share a page."""
    return f"""
<svg class="{css_class}" viewBox="0 0 64 64" role="img" aria-label="BUZZ-WISE bee">
  <defs>
    <clipPath id="body-{uid}"><ellipse cx="32" cy="39" rx="14.5" ry="18.5"/></clipPath>
  </defs>
  <g class="bee-fly">
    <!-- wings -->
    <g class="wing wing-l">
      <ellipse cx="19" cy="22" rx="12" ry="8.5" transform="rotate(-30 19 22)" fill="#DDF0FB" stroke="#14324B" stroke-width="2.2"/>
    </g>
    <g class="wing wing-r">
      <ellipse cx="45" cy="22" rx="12" ry="8.5" transform="rotate(30 45 22)" fill="#DDF0FB" stroke="#14324B" stroke-width="2.2"/>
    </g>

    <!-- antennae -->
    <path d="M28.5 21.5 C27.5 15 26 10.5 23.5 7.5 M35.5 21.5 C36.5 15 38 10.5 40.5 7.5"
          fill="none" stroke="#14324B" stroke-width="2.2" stroke-linecap="round"/>
    <circle cx="23.5" cy="7.5" r="2.2" fill="#14324B"/>
    <circle cx="40.5" cy="7.5" r="2.2" fill="#14324B"/>

    <!-- stinger -->
    <path d="M29.5 56.5 L32 62 L34.5 56.5 Z" fill="#14324B" stroke="#14324B" stroke-width="1.2" stroke-linejoin="round"/>

    <!-- body, stripes kept inside the outline -->
    <ellipse cx="32" cy="39" rx="14.5" ry="18.5" fill="#F4B63F"/>
    <g clip-path="url(#body-{uid})" fill="#14324B">
      <path d="M10 31.5 Q32 35 54 31.5 V36 Q32 39.5 10 36 Z"/>
      <path d="M10 41 Q32 44.5 54 41 V45.5 Q32 49 10 45.5 Z"/>
      <path d="M10 49.5 Q32 53 54 49.5 V53.5 Q32 57 10 53.5 Z"/>
      <ellipse cx="26" cy="27" rx="4" ry="2.4" fill="#fff" opacity=".45" transform="rotate(-30 26 27)"/>
    </g>
    <ellipse cx="32" cy="39" rx="14.5" ry="18.5" fill="none" stroke="#14324B" stroke-width="2.4"/>
  </g>
</svg>"""


BEE_CSS = """
.bee .bee-fly{animation:bob 2.6s ease-in-out infinite;transform-box:view-box;transform-origin:32px 38px}
.bee .wing{transform-box:view-box;animation:flap .14s ease-in-out infinite alternate}
.bee .wing-l{transform-origin:27px 27px}
.bee .wing-r{transform-origin:37px 27px;animation-name:flap-r}
@keyframes flap{from{transform:rotate(0)}to{transform:rotate(14deg)}}
@keyframes flap-r{from{transform:rotate(0)}to{transform:rotate(-14deg)}}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-2px)}}
@media (prefers-reduced-motion:reduce){.bee .bee-fly,.bee .wing{animation:none}}
"""
