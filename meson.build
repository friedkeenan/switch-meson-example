project('demo', 'c',
    version : '1.0.0',
)

source_dirs = ['source']
includes    = []
defines     = []
romfs       = 'romfs'

npdm_json = 'config.json'

author = 'Unspecified Author'
icon   = 'icon.jpg'

dependencies = []

no_nacp = false

dkp = run_command('sh', '-c', 'echo -n $DEVKITPRO').stdout() # Needs sh -c for some reason
if dkp == ''
    error('Please set DEVKITPRO in your environment. export DEVKITPRO=<path to>/devkitpro')
endif

libnx = meson.get_compiler('c').find_library('nx',
    dirs : dkp + '/libnx/lib'
)

includes += dkp + '/libnx/include' # Not happy with this
dependencies += libnx

sources = []
foreach s : source_dirs
    subdir(s)
endforeach

arch = ['-march=armv8-a+crc+crypto', '-mtune=cortex-a57', '-mtp=soft']

c_args = ['-g', '-Wall', '-O2', '-ffunction-sections', '-D__SWITCH__'] + arch + defines
cpp_args = c_args + ['-fno-rtti', '-fno-exceptions']

link_args = ['-specs=' + dkp + '/libnx/switch.specs', '-g', '-fPIE'] + arch

exe = executable(meson.project_name() + '.elf', sources,
    include_directories : includes,
    dependencies        : dependencies,

    c_args    : c_args,
    cpp_args  : cpp_args,
    link_args : link_args,

    pie : true,
)

fs = import('fs')

if not fs.is_file(icon)
    icon = dkp + '/libnx/default_icon.jpg'
endif

output = ''
cmd = [files('build.py'),
    '--out-dir', '@OUTDIR@',
    '--input',   '@INPUT@',
    '--output',  '@OUTPUT0@',
    '--tmp-dir', '@PRIVATE_DIR@',
]

if not fs.is_file(npdm_json)
    output = meson.project_name() + '.nro'

    if fs.is_dir(romfs)
        cmd += ['--romfs', files(romfs)]
    endif

    cmd += ['--icon', files(icon)]

    if not no_nacp
        cmd += [
            '--name',    meson.project_name(),
            '--author',  author,
            '--version', meson.project_version(),
        ]
    else
        cmd += ['--no-nacp']
    endif
else
    output = meson.project_name() + '.nsp'

    cmd += ['--npdm-json', files(npdm_json)]
endif

custom_target(output,
    output  : [output, output + '@cus'],
    input   : exe,
    command : cmd,

    build_by_default : true,
)