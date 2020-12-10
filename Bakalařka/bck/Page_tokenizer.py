"""
Author: Jiri Matejka (xmatej52)

V tomto modulu je implementovan proces tokenizace.
"""

import os, signal
import multiprocessing
import subprocess
import re
import time
import sys
import langdetect
import Functions
from Page_reader import Page_reader
from Page import Page

TIMEOUT_FOR_TERMINATE = 15

class Page_tokenizer( object ):
    """
    Trida pomoci ktere lze proves tokenizaci, detekci jazyka a prevod do vertikalni podoby.
    """
    def __init__( self, tokenizer_bin, filename = None, language = 'generic', processes = 10, lang_detect = False, old_style = False ):
        self._page_reader = Page_reader( filename, old_style = old_style )
        self._tokenizer_bin  = tokenizer_bin

        # Nastavime jazyk tokenizace, rozdily jsou minimalni
        if ( language == 'english' or language == 'czech' ):
            self._detect = language
        else:
            self._detect = 'generic'

        self._processes = processes
        self._langdetect = lang_detect
        self._errors_queue = multiprocessing.Queue()
        self._errors_info = []

    @staticmethod
    def _translator( input_paragraphs, output_languages ):
        # Metoda je urcena pro proces provadejici preklady.
        par = ''
        while ( True ):
            # nacteme novy text
            par = input_paragraphs.get()
            # None znaci konec zpracovani, jinak pokracujeme
            if ( par is not None ):
                lang = ''
                # Detekce jazyka je narocny proces a nema smysl ji provadet na kratsich retezcich
                if ( len( par ) > 10 ):
                    try:
                        # pokusime se o detekci jazyka
                        lang = langdetect.detect( par )
                    except:
                        # nezdarilo se
                        lang = None
                else:
                    # retexec je prilis kratky
                    lang = None
                output_languages.put( lang )
            else:
                break
        # Tohle by se delat nemelo, ale cert to vem. Je to prakticke.
        # je to tu kvuli tomu, aby funkce neskoncila drive, nez se ulozi zaznam do fronty
        time.sleep(0.1)

    def _tokenizer( self, input_queue, output_queue ):
        # Metoda urcena pro proces vertikalizace
        command = [ self._tokenizer_bin, '--tokenizer=' + self._detect, '--output=vertical' ]
        # vytvorime fronty pro prekladac
        translator_inqueue  = multiprocessing.Queue()
        translator_outqueue = multiprocessing.Queue()
        while ( True ):
            # nacteme vstupni data
            page = input_queue.get()
            send_buff = ''
            # None znaci konec zpracovani
            if ( page is not None ):
                removed = list()
                tmp      = ''
                new_page = ''
                # nejprve extrahujeme text ze stranky a ten rozdelime na radky
                for line in page.get_text().splitlines():
                    # nahradime divy za paragrafy
                    if ( re.match( r'</?doc.*>|<img.*>|</?link.*>|</?head>|</?p>|</?div>|</?h[1-5]>', line ) ):
                        if ( line == '<div>' ):
                            line = '<p>'
                        elif ( line == '</div>' ):
                            line = '</p>'
                        new_page += tmp + line + '\n'
                        tmp = ''
                        continue
                    # a take vlozime </g> kde je treba.
                    else:
                        line = re.sub( r'([\w])([^\w\s])|([^\w\s])([\w])', r'\1\3\n<g/>\n\2\4', line )
                    tmp += line  + '\n'

                # uz nepotrebujeme zpracovanou stranku, smazeme data a tim uvolnime trochu pameti
                page.clear()

                # Rozpracovanou stranku musime znovu projit... V jednom cyklu se mi to nepodarilo udelat...
                jump_behind_tag = ''
                for line in new_page.splitlines():
                    if jump_behind_tag:
                        if line.startswith(jump_behind_tag):
                            jump_behind_tag = ''
                        continue
                    # Detekujeme tagy a zakodujeme je. Tokenizer by jinak uplne rozbil zpracovani
                    if ( re.match( r'</?doc.*>|<img.*>|</?link.*>|</?head>|</?p>|</?h[1-5]>|<g/>', line ) ):
                        if ( line.startswith( '<link' ) ):
                            try:
                                removed.append( '="' + page.get_absolute_url( line[7:] ) )
                            except ValueError:
                                # Pokud selže page.get_absolute_url přeskočíme vadný link
                                jump_behind_tag = '</link>'
                                continue
                            line = '<link>'
                        elif ( line.startswith( '<img' ) ):
                            try:
                                removed.append( '="' + page.get_absolute_url( line[6:] ) )
                            except ValueError:
                                # Pokud selže page.get_absolute_url přeskočíme vadný img
                                jump_behind_tag = '</img>'
                                continue
                            line = '<img>'
                        elif ( line.startswith( '<doc' ) ):
                            removed.append( line[4:] )
                            line = '<doc>'
                        line = Page.encode_tag( line )
                    send_buff += line + '\n'

                # Pokud je zapla detekce jazyka, spustime proces provadejici detekci.
                if ( self._langdetect ):
                    multiprocessing.Process( target = self._translator, args = ( translator_inqueue, translator_outqueue ) ).start()

                # spustime tokenizer
                process = subprocess.Popen( command, stdout=subprocess.PIPE, stdin=subprocess.PIPE )

                # pokusime se zpracovat stranku s nastavenym timeoutem.
                # 0.5 sekundy je vic nez dostacujici doba (ale ne kdyz je prilis vytizeny stroj). Vetsinou se nezdari zpracovat stranky ve formatu PDF nebo online vysilani
                # Ty tokenizer je schopen zpracovavat i nekolik hodin.
                try:
                    ret_value = process.communicate( send_buff.encode(), timeout=4 )[0].decode()
                except subprocess.TimeoutExpired:
                    error = Functions.get_exception_info( 'Stranku se nepodarilo se nepodarilo zpracovat behem 4 sekund - "' + page.get_url() + '".' )
                    self._set_error( message = error, page_id = page.id)
                    process.kill()
                    # ret_value = process.communicate()[0].decode() # z neznámého důvodu mi způsobil deadlock
                    process.poll()
                    ret_value = ""

                replaced  = ''
                sentence  = 0 # 0 - mimo vetu, 1 - ve vete, 3 - ukoncit
                paragraph = 0 # 0 - mimo, 1 - mozna zacina, 2 - unvnitr, 3 - ukoncit
                link_len  = -1
                odeslano  = 0
                translator_buffer = ''
                link_str = ''
                # Nyni musime znovu dat dohromady vertikalizovany text. Musime doplnit vety a odstavce tam, kde chybi.
                for line in ret_value.splitlines():
                    # Detekujeme tag
                    if ( line.startswith( Page.tag_begin ) ):
                        # Dekodujeme tag do puvodni podoby
                        line = Page.decode_tag( line )
                        if ( paragraph == 2 and re.match( r'<(/?p|/?h[1-5]|/?head|/?doc)>', line ) ):
                            # Jsme uvnitr odstavce a je ho treba ukoncit
                            paragraph = 0
                            if ( line == '<p>' ):
                                paragraph = 1
                            elif ( line == '<doc>' ):
                                rest = removed.pop(0)
                                line = '<doc' + rest
                            if ( line != '</p>' ):
                                line = '</p>\n' + line
                            if ( sentence == 1 ):
                                line = '</s>\n' + line
                                sentence = 0
                        else:
                            # Vlozime odebrane tagy
                            if ( line == '<p>' or line == '</p>' ):
                                # prazdne odstavce s zignoruji
                                continue
                            elif ( line == '<link>' ):
                                rest = removed.pop(0)
                                link_str = '<link' + rest
                                link_len = 0
                                continue
                            elif ( line == '<doc>' ):
                                rest = removed.pop(0)
                                line = '<doc' + rest
                            elif ( line == '<g/>' and replaced[-5:-1] == '</s>' ):
                                replaced = replaced[:-5] + '<g/>\n</s>\n'
                                continue
                            elif ( line == '<img>' ):
                                rest = removed.pop(0)
                                line = '<img' + rest + '\t<lenght=1>'
                                if ( paragraph == 0 ):
                                    line = '<p>\n<s>\n' + line
                                paragraph = 2
                            elif ( line == '</link>' ):
                                if ( len( link_str ) == 0 ):
                                    continue
                                if ( link_len < 0 ): # Obcas nejaky chytrak da odkaz dovnitr odkazu...
                                    link_len = 0
                                if ( paragraph == 0 ):
                                    link_str = '<p>\n<s>\n' + link_str
                                elif ( sentence == 0 ):
                                    if ( replaced[-5:-1] == '</s>' ):
                                        replaced = replaced[:-5]
                                    else:
                                        link_str = '<s>\n' + link_str
                                paragraph = 2
                                sentence  = 1
                                line = link_str + '\t<lenght=' + str( link_len ) + '>'
                                link_len = -1
                            elif ( paragraph == 1 and line == '</doc>' ):
                                replaced = replaced[:-4]
                    else:
                        # vlozime slovo do detekce jazyka, pokud je detekce zapnuta
                        if ( self._langdetect ):
                            translator_buffer += line + '\n'

                        # pokud se nejedna o prazdny radek, doplnime vety a paragraph
                        if ( len( line ) > 0 ):
                            if ( sentence == 0 ):
                                line     = '<s>\n' + line
                                sentence = 1
                            if ( paragraph == 0 ):
                                line = '<p>\n' + line
                                paragraph = 2
                            elif ( paragraph == 1 ):
                                paragraph = 2
                        # pokud se jedna o prazdny radek, vetu ukoncime
                        elif ( sentence == 1 ):
                            line = '</s>' + line
                            sentence = 0

                    # zvisime pocitadlo delky odkazu
                    if ( link_len >= 0 ):
                        link_len += 1

                    # pokud ukoncujeme odstavec, odesleme text k prekladu
                    if ( self._langdetect and '</p>' in line ):
                        odeslano += 1
                        translator_inqueue.put( translator_buffer )
                        translator_buffer = ''
                 
                    replaced += line + '\n'

                # Pote co mame vertikalizovany text, je treba doplnit jazyky k odstavcum.
                if ( self._langdetect ):
                    translated = ''
                    tag_p_flag=0
                    tag_p_flag_end=1

                    # rekneme detekci jazyka, ze je cas jit spat (ne vazne, on si fakt pak pujde dat slofika na 0.1 sekundy)
                    translator_inqueue.put( None )
                    xtest=''+replaced
                    xtestlist=[]

                    
                    for lineid,line in enumerate(replaced.splitlines()):
                        if(page.get_url() == 'https://economictimes.indiatimes.com/markets/stocks/news/dhfl-hits-upper-circuit-as-adani-group-piramal-oaktree-bid-for-firm/articleshow/78744442.cms'):
                            if(odeslano==0):
                                tag_p_flag_end=0

                        #kontrola jestli byl predchozi odstavec ukoncen pred zacatkem dalsiho odstavce
                        if (line == '</p>'):
                            tag_p_flag=0
                        #if(odeslano == 5):
                            #if(page.get_url() == 'https://economictimes.indiatimes.com/markets/stocks/news/dhfl-hits-upper-circuit-as-adani-group-piramal-oaktree-bid-for-firm/articleshow/78744442.cms'):
                            #    sys.stderr.write('==========================='+'\n')
                            #    sys.stderr.write(xtest+'\n')
                            #    sys.stderr.write('=========================='+'\n')
                        #if(page.get_url() == 'https://economictimes.indiatimes.com/markets/stocks/news/dhfl-hits-upper-circuit-as-adani-group-piramal-oaktree-bid-for-firm/articleshow/78744442.cms'):
                        if(odeslano == 0):
                            #if(page.get_url() == 'https://economictimes.indiatimes.com/markets/stocks/news/dhfl-hits-upper-circuit-as-adani-group-piramal-oaktree-bid-for-firm/articleshow/78744442.cms'):
                            #    sys.stderr.write(xtest+'\n')
                            for lineid2,line2 in enumerate(xtest.splitlines()):
                                if(lineid2 >= lineid):                           
                                    if('</p>' in line2):
                                        tag_p_flag_end=0
                            #if(page.get_url() == 'https://economictimes.indiatimes.com/markets/stocks/news/dhfl-hits-upper-circuit-as-adani-group-piramal-oaktree-bid-for-firm/articleshow/78744442.cms'):
                            #    for x in xtestlist:
                            #        sys.stderr.write('asdddsa   ='+str(x)+'\n')

                            #if('</p>' not in xtestlist):
                            #    tag_p_flag_end=0


                        # narazili jsme na odstavec
                        if ( line == '<p>' and tag_p_flag == 0 and tag_p_flag_end == 1 ):
                            tag_p_flag=1
                            
                            #check jestli v textu na zpracovani je konec odstavce
                            # jednou se mi stalo, ze mi nesedel poced odstavcu a prelozenych textu - coz znamenalo DEADLOCK
                            if ( odeslano == 0 ):
                                error = Functions.get_exception_info( 'Zabranuji DEADLOCKU a odstranuji stranku "' + page.get_url() + '" ze zpracovani.' )
                                self._set_error( message = error, page_id = page.id)
                                break
                            # ale vetsinou je to vsechno cajk
                            else:
                                lang = translator_outqueue.get()
                                odeslano -= 1
                                if ( lang ):
                                    line = '<p lang="' + lang + '">'
                        translated += line + '\n'
                    # kdyz uz jsou jazyky poznamenany, tak to odesleme
                    output_queue.put( translated )
                    # Protoze se mi jednou stalo ze mi nesedel pocet odstavcu, radeji dam kontrolu kdybych jich prelozil vic nez jich ve skutecnosti mam.
                    if ( odeslano != 0 ):
                        error = Functions.get_exception_info( 'Nebylo vse prelozeno. "' + str( page.id ) + '".' )
                        self._set_error( message = error, page_id = page.id)
                else:
                    # odesleme vysledek - bez detekce jazyka
                    output_queue.put( replaced )
            else:
                # Vypneme se
                output_queue.put( None )
                time.sleep( 0.1 ) # Tohle by se delat nemelo - je to tu jen pro jistotu
                break

    def __iter__( self ):
        input_queue  = multiprocessing.Queue()
        output_queue = multiprocessing.Queue()

        # nastartujeme procesy
        child_processes = []
        for i in range( self._processes ):
            p = multiprocessing.Process( target = self._tokenizer, args = ( input_queue, output_queue ) )
            child_processes.append(p)
            p.start()

        # zacneme posilat data procesum
        for page in self._page_reader:
            input_queue.put( page )
            try:
                while ( True ):
                    # vratime data hned, jak budeme moci
                    yield output_queue.get( block = False )
            except:
                pass

        # Kazdemu procesu rekneme, at se ukonci
        for i in range( self._processes ):
            input_queue.put( None )

        # uzavreme frontu
        input_queue.close()

        # nacteme zbytek dat
        cond = self._processes
        while ( cond > 0 ):
            try:
                tokenized = output_queue.get(timeout=60)
                self._update_errors_info()
                if ( tokenized is not None ):
                    yield tokenized
                else:
                    cond -= 1
            except multiprocessing.queues.Empty:
                # Nezískáme-li odpověď, musíme zkontrolovat, zda-li nějaký proces neumřel nelegálně
                if any(p.exitcode != 0 for p in child_processes if not p.is_alive()):
                    # Pokud ano, ukončíme zbytek procesů a ukončíme zpracování
                    error = Functions.get_exception_info('Nektery z procesu umrel.')
                    self._set_error(message = error, page_id = 'N/A')
                    for p in child_processes:
                        if p.is_alive():
                            p.terminate()
                            p.join(TIMEOUT_FOR_TERMINATE)
                            if p.is_alive():
                                os.kill(p.pid, signal.SIGKILL)
                            p.join()
                    break
        
        self._update_errors_info()
        
        # pockame na vlakna
        input_queue.join_thread()
        # uzavreme frontu
        output_queue.close()
        # pockame na vlakna
        output_queue.join_thread()

    def _set_error( self, message, page_id ):
        self._errors_queue.put_nowait('-ERR ' + page_id + '\n-ERR_START\n' + message + '-ERR_END\n')

    def _update_errors_info(self):
        try:
            while True:
                self._errors_info.append(self._errors_queue.get_nowait())
        except multiprocessing.queues.Empty:
            pass

    def get_errors_info( self ):
        """
        Vrati seznam chyb jako retezec.
        """
        self._update_errors_info()
        message = "".join(self._errors_info)
        self._errors_info.clear()
        return message

if __name__ == '__main__':
    # input_file tagger_bin tagger_file timeout
    parser = Page_tokenizer( tokenizer_bin = sys.argv[2], filename = sys.argv[1], lang_detect = True, processes = 10)
    for tagged in parser:
        print( tagged )
        #pass
