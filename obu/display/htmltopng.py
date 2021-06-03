# -*- coding: utf-8 -*-
import pdfcrowd
import sys

# html to png
def change_htmltopng (htmlfile):
    try:
        # create the API client instance
        client = pdfcrowd.HtmlToImageClient('demo', 'ce544b6ea52a5621fb9d55f8b542d14d')
        # configure the conversion
        client.setOutputFormat('png')
        # run the conversion and write the result to a file
        client.convertFileToFile('display/html/'+htmlfile, 'display/image/map.png')
    except pdfcrowd.Error as why:
        # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))
        # rethrow or handle the exception
        raise