gzinflatekiller
===============

Hunt through PHP files containing an eval(gzinflate(base65_decode())) virus
---------------------------------------------------------------------------

You may come across a nasty virus one day that executes and runs recursively across all of your PHP files, 
infecting everyone of them. This can be quite a tricky one to get past, especially as the files keep coming back, 
the singature will look similar to the following, and will be prepended to the top of the file in plain site:
  <?php eval(gzinflate(base64_decode(xxx)));?>

How do we kill it? The following is a little Python script I've written that has worked successfully for myself
(I wrote this to take care of an infection that happened where I work) The Patterns constant defines "\r\n" and 
the signature as the patterns to check for, this is because the virus left several "\r\n" in it's wake, so you 
may want to remove that pattern from the script if you use windows style new lines.



Steps
=====

    1: Disable your webserver so that the files are prevented from running, after all, running 
       any infected file will affect every other file again putting your efforts in vain.

    2: Run the python script, like the following: $ ./gzinflatekiller.py  "/var/www"    
       (The script will run recursively and touch any php files or file types listed in the EXT constant)

    3: You may need to also disable the gzinflate function, or even exec all together which is always 
       a security risk: Go into /etc/php.ini or your respective PHP Ini File and add the following line, 
       or append:  disable_functions = gzinflate

    4: Now turn your web server back on and this should do the trick. You may also want to run a rkhunter 
    and a maldet scanner just to be sure, you may end up finding the insertion point this way, either way, 
    that virus will no longer be able to execute anymore. 
    
NOTE!
=====
although previously mentioned it may have been missed but:
One of the regular expressions matches \r\n lines, this is because it left a trail of these beneath the infection,
remove this regular expression from the PATTERNS variable if you want to retain these in your files, you may use
these and they may be important to you.
