#usr/bin/env bash

RELEASE=3.13.0-44-generic
KBUILD="/lib/modules/$RELEASE/build";
NEW_KBUILD=/home/scudette/rekall/tools/linux/lmap/build/kernel_headers

# link all contents of kbuild, but copy Makefile
for FILE in `ls -AHL $KBUILD`
do
  if [ $FILE == "Makefile" ]
  then
    # Copy the Makefile, we need to modify this later
    cp $KBUILD/$FILE $NEW_KBUILD
  else
    ln -s $KBUILD/$FILE $NEW_KBUILD
  fi
done

# disable the ftrace gcc option
sed -i "s/^ifdef CONFIG_FUNCTION_TRACER$/ifdef THIS_OPTION_HAS_BEEN_DISABLED/g" $NEW_KBUILD/Makefile
