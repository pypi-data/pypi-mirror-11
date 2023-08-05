NAME

    mnamr - rename movie directories

SYNOPSIS

    mnamr [-h] [dir]

DESCRIPTION

    mnamr renames your movie directories according to the following naming
    convention:

        <Title> (<Year>) imdb:<imdb-id>

    On installation, the `mnamr` executable is made available on your PATH. Run
    it from any directory to rename all its immediate subdirectories.

    mnamr tries to parse the movie title from existing unknown folders and uses
    imdbpie to search for the correct movie on iMDB. The console will let you
    search for different terms or enter the iMDB ID manually.

INSTALLATION

    [sudo] pip install mnamr

USAGE

    $ cd folder-with-lots-of-movie-dirs/
    $ mnamr
    $ # follow the instructions
