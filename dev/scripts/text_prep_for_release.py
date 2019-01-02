release_pars_op = op('button_save_for_release')
base_release_tox = release_pars_op.par.Targetoperator
version = 'v.{}'.format(release_pars_op.par.Version)
reset_color = (0.545, 0.545, 0.545)
save_loc = '{loc}/{name}.tox'.format(loc=release_pars_op.par.Savelocation, name=release_pars_op.par.Toxname)
destory_tags = release_pars_op.par.Destroytags.val.split(",")
mods_and_ext_ops = base_release_tox.findChildren(tags=['EXT', 'MOD'])
destroy_ops = base_release_tox.findChildren(tags=destory_tags)

# save tox
# set version
base_release_tox.par.Version = version

for each in mods_and_ext_ops:
    # remove path par for ext
    each.par.file = ''
    # turn off loading on start
    each.par.loadonstart = False

# remove path for extenral tox
base_release_tox.par.externaltox = ''

# set the color to something neutral
base_release_tox.color = reset_color

# lock the tox for the icon
base_release_tox.op('null_icon').lock = True

# destroy all dev ops
for each in destroy_ops:
    base_release_tox.op(each).destroy()

# save the tox
base_release_tox.save(save_loc)