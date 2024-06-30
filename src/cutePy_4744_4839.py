#$VASILEIOS IOANNIS BOUZAMPALIDIS, AM:4744 username: cse94744
#$ALEXANDROS AGAPITOS CHRISTODOULOU, AM:4839 username: cse94839




import sys
import inspect

quad_length_list=1

class Special_words:
    def __init__(self):
        self.family_type=["id","keyword","number","mathOperator","relOperator","bool_operator","delimiter","groupSymbol","assignment","eof"]
        
        self.letters="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUWXYZ#"
        self.numbers="0123456789"
        
        self.keywords=["if","else","elif","while","return","print","input","#def","def","#int","int","global"]

        self.bool_operators=["not","or","and"]
        self.math_operators=["+","-","*","//","%"]

        self.assignment="="
        
        self.rel_operators=["==",">=","<=","<",">","!="]
        self.delimiters=[",",":"]
        self.group_symbol=["(",")","#{","#}"] 
        self.whitespaces=["\t","\n","\r"," "]
        
class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string=recognized_string
        self.family=family
        self.line_number= line_number
              
class Lex:
    def __init__(self, file_name):
        self.file_name=file_name
        self.current_line=0
        self.tokens=[]
        self.token_id="" 
        self.comment_detected=False
        self.rel_detected=False

        print("------------------------")
        print("Lectical Analysis")
        print("------------------------")
        
    def __error(self, s):
        print(s,self.current_line)
        sys.exit()
        
        
    def next_token(self):
        return self.tokens[0]
    
    def __del__(self):
        try:
            self.tokens.pop(0)
        except:
            print()
        
  
    def lex(self):
        current_char=""
        letter_detected=False
        with open(self.file_name,encoding="utf-8") as file:
            for line in file:
                self.current_line+=1

                for next_char in line:  
                    self.__check(current_char, next_char, letter_detected)
                    current_char=next_char

            self.__check(current_char, "eof", letter_detected) #eof is used to assign a null like value to next_char instead of using None. Comparing a string to a character always returns false (WORKS LIKE None)
            if(self.comment_detected):
                self.__error("Error: Comment Brackets '##' Never Closed")
            self.tokens.append(Token("","eof", -1))


    def __check(self,current_char, next_char, letter_detected):   
        if(self.comment_detected):
            if(current_char+next_char=="##"):
               self.token_id+=current_char 
            elif(self.token_id=="#" and current_char=="#"):
                self.token_id=""
                self.comment_detected=False
                
        elif(current_char+next_char=="##"):#checks if there are comments and ignores them
            self.comment_detected=True
            #self.token_id+=current_char
 
        elif(current_char in Special_words().whitespaces):
            self.token_id=""

        #checks for letter
        elif(((current_char in Special_words().letters and current_char!="" and (current_char+next_char!="#{" and current_char+next_char!="#}" and current_char not in "}{")) or letter_detected)):
        
            self.token_id+=current_char
            letter_detected=True
            if(self.token_id!=""):
                if(next_char not in Special_words().letters and next_char not in Special_words().numbers):
                    if("#" in self.token_id and self.token_id!="#int" and self.token_id!="#def"):
                        self.__error('Error: Illegal character combination used: "'+self.token_id+'", line:')

                    self.tokens.append(self.create_token(self.token_id))
                    self.print_last_token()
                    letter_detected=False
                    self.token_id=""

        #checks for numbers   
        elif(current_char in Special_words().numbers):
            self.token_id+=current_char
            if(self.token_id!=""):
                if(next_char not in Special_words().numbers):
                    self.tokens.append(self.create_token(self.token_id))
                    self.print_last_token()
                    self.token_id=""

        #checks for math operators
        elif(current_char in Special_words().math_operators or current_char=="/"):
            self.token_id+=current_char
            if(self.token_id=="/" and next_char!="/"):
                self.__error('Error: Illegal math operator used: '+'"'+self.token_id+'" operator not recognized (did you mean "//" ?), line:')#edo exei error epeidi den iparxei / sketo
            elif(self.token_id=="/" and next_char=="/"):
                pass
            else:
                self.tokens.append(self.create_token(self.token_id))
                self.print_last_token()
                self.token_id=""
            
        #checks for rel operators
        elif(current_char  in Special_words().rel_operators or self.rel_detected or (current_char+next_char in Special_words().rel_operators)):
            
            self.token_id+=current_char
            if(current_char+next_char in Special_words().rel_operators):
                self.rel_detected=True
            else:
                self.tokens.append(self.create_token(self.token_id))
                self.print_last_token() 
                self.token_id=""
                self.rel_detected=False
        
        #checks for assignment
        elif(current_char==Special_words().assignment):
            self.token_id=current_char
            self.tokens.append(self.create_token(self.token_id))
            self.print_last_token()
            self.token_id=""

        #checks for delimiters
        elif(current_char in Special_words().delimiters): 
            self.token_id=current_char
            self.tokens.append(self.create_token(self.token_id))
            self.print_last_token() 
            self.token_id=""
            
        #checks for parenthesis
        elif(current_char in Special_words().group_symbol or current_char=="#" or current_char=="{" or current_char=="}"):
            self.token_id+=current_char
            if(self.token_id+next_char == "#{" or self.token_id+next_char == "#}"):
                pass
            elif(self.token_id== "#" and (next_char != "{" or next_char != "}")):
                self.__error('Error: Illegal character combination used:'+'"'+self.token_id+next_char+'", line:')
            elif(self.token_id=="{" or self.token_id=="}"): 
                self.__error('Error: Illegal character used:'+'"'+self.token_id+'" expected "#" before "'+ self.token_id+'", line:')
            else:
                self.tokens.append(self.create_token(self.token_id))
                self.print_last_token() 
                self.token_id=""
        else:
            
            self.__error('Error: Illegal character used: '+'"'+current_char+'" character not supported, line:')
        return

    def create_token(self, s):             
        if(s in Special_words().keywords):
            return Token(s,"keyword", self.current_line)
        elif (s in Special_words().bool_operators):
            return Token(s,"bool_operator", self.current_line)
        elif(s.isnumeric()):
            return Token(s,"number",self.current_line)
        elif(s in Special_words().math_operators):
            return Token(s,"mathOperator",self.current_line)
        elif(s in Special_words().rel_operators):
            return Token(s,"relOperator",self.current_line)
        elif(s==Special_words().assignment):
            return Token(s,"assignment",self.current_line)
        elif(s in Special_words().delimiters):
            return Token(s,"delimiters", self.current_line)
        elif(s in Special_words().group_symbol):
            return Token(s,"groupSymbol", self.current_line)
        else:
            return Token(s,"id",self.current_line)
        

    def print_last_token(self):
        print(self.tokens[len(self.tokens)-1].recognized_string,end='  family: "')
        print(self.tokens[len(self.tokens)-1].family,end='", line: ')
        print(self.tokens[len(self.tokens)-1].line_number)


class Syntax:

    # BASIC METHODS

    def __init__(self,file_name):
        self.lexical_anal = Lex(file_name)
        self.lexical_anal.lex()
        self.keep_line = 0
        self.inter = Inter_Code()
        self.expression_list=[]
        
        self.function_names=[]
        print("------------------------")
        print("Syntax Analysis")
        print("------------------------")
        self.symbol_table=Table()
        
        
        self.final = FinalCode(self.symbol_table,self.inter.temp_variables_list)
        
        
    def get_token(self):
        self.token = self.lexical_anal.next_token()
        self.lexical_anal.__del__()
        return self.token

    def error(self,s): 
        print("\nSyntaxError: invalid syntax")
        print(s+', line:',self.token.line_number,'\n')
        sys.exit()

    def start_rule(self): 
        self.token= self.get_token()

        while(self.token.family!="eof"):    
            if(self.token.recognized_string == "def"):
                self.token= self.get_token()
                self.def_function()
                
            elif(self.token.recognized_string == "#def"):
                self.token= self.get_token()
                self.def_main_part()
            elif(self.token.recognized_string=="#int"):
                self.declarations()
            else:
                self.error("Invalid Declaration of function or variable")
        if self.inter.main_name=="":
            self.inter.main_name=str(int(self.inter.nextquad())-1)
            self.final.final_code_list.insert(4,("j L_"+self.inter.main_name))
            
        self.inter.create_inter_file()
        self.keep_line=self.final.createFinalCode(self.inter.quad_list, self.inter.main_name,self.keep_line)
        self.final.create_assembly_file()
        self.symbol_table.remove_level()  

    def def_main_part(self):
        self.def_main_function()
        while self.token.recognized_string == "def":
            self.token= self.get_token()
            self.def_main_function()
            
########################
    def def_main_function(self):
        function_name=self.token.recognized_string
        self.inter.main_name=function_name
        if self.token.family == Special_words().family_type[0]:
            self.token= self.get_token()
            self.declarations()
            while self.token.recognized_string == "def":
                self.token= self.get_token()
                self.def_function()
            self.inter.begin_block(function_name)
            self.statements()             
        else:
            self.error('Illegal function name')
            
          
        quad=self.inter.genquad("halt", "_", "_", "_")
        self.inter.add_to_list(quad)
        
        self.inter.end_block(function_name)
        
        
########################      
    

    def def_function(self):
        function_name=self.token.recognized_string
        function=Function(function_name,"integer","","")
        
        self.symbol_table.add_rec(function)
        self.symbol_table.add_level()

        self.function_names.append(function_name)
        
        if self.token.family == Special_words().family_type[0]:
            self.token= self.get_token()
            if self.token.recognized_string == "(":
                self.token= self.get_token()
                self.id_list("function")
                self.symbol_table.update_formal_parameters(function_name,self.symbol_table.formal_par_list)
                self.symbol_table.formal_par_list.clear()
                
                if self.token.recognized_string == ")":
                    self.token= self.get_token()
                    if self.token.recognized_string == ":":
                        self.token= self.get_token()
                        if self.token.recognized_string == "#{":
                            self.token= self.get_token()
                            self.declarations()
                            self.globals()
                            
                            while self.token.recognized_string == "def":
                                self.token= self.get_token()
                                self.def_function()
                                
                            self.inter.begin_block(function_name)
                            self.symbol_table.update_starting_quad(function_name,self.inter.nextquad)
                            
                            self.globals()
                            self.statements()
                            
                            if self.token.recognized_string == "#}":
                                self.token= self.get_token()
                                self.inter.end_block(function_name)
                            else:
                                self.error('Illegal function implementation: expected: "#}" to end function')
                        else:
                            self.error('Illegal function implementation: expected: "#{"')
                    else:
                        self.error('Expected ":" after declaring a function')
                else:
                    self.error('Expected: ")" to end declaration of function')
                    
            else:
                self.error('Expected: "(" when declaring a function')
        else:
            self.error('Illegal function name')
        frameLength=self.symbol_table.offsets[len(self.symbol_table.offsets)-1]
        
        self.symbol_table.update_frameLength(function_name,frameLength)
        
        self.keep_line=self.final.createFinalCode(self.inter.quad_list, self.inter.main_name,self.keep_line)
        self.symbol_table.remove_level()

    def globals(self):
        while self.token.recognized_string=="global":
            self.global_line()
    
    def global_line(self):
        if self.token.recognized_string == "global":
            self.token=self.get_token()
            self.id_list("global")
        else:
            self.error("illegal declaration name")
            
    def declarations(self):
        while self.token.recognized_string == "#int":
            self.declaration_line()

    def declaration_line(self):
        if self.token.recognized_string == "#int":
            self.token=self.get_token()
            self.id_list("#int")
        else:
            self.error("illegal declaration name")
    
    def statement(self):
        if self.token.recognized_string == "print" or self.token.recognized_string == "return" or self.token.family == Special_words().family_type[0]:
            self.simple_statement()
        elif self.token.recognized_string == "if" or self.token.recognized_string == "while":
            
            self.structured_statement()
        else:
            self.error("Token not recognized")

    def statements(self):
        
        self.statement()
        while self.token.recognized_string == "print" or self.token.recognized_string == "return" or self.token.family == Special_words().family_type[0] or self.token.recognized_string == "if" or self.token.recognized_string == "while":
            self.statement()
        

    def simple_statement(self):
        
        if self.token.recognized_string == "print":
            self.token=self.get_token()
            self.print_stat()
        elif self.token.recognized_string == "return":
            self.token=self.get_token()
            self.return_stat()
        elif self.token.family == Special_words().family_type[0]:
            
            
            self.assignment_stat()
            
        else:
            self.error("Token not recognized")

    def structured_statement(self):
        if self.token.recognized_string == "if":
            self.token= self.get_token()
            self.if_stat()
        elif self.token.recognized_string == "while":
            self.token= self.get_token()
            self.while_stat()
        else:
            self.error('Keyword not recognized: Expected: "if" or "while"')
    
    def assignment_stat(self): 
        inp=self.token.recognized_string
        self.expression_list.append(inp)
        
        var=Variable(self.token.recognized_string, "integer", self.symbol_table.offsets[len(self.symbol_table.table)-1])
        self.symbol_table.add_rec(var)
        
        self.token=self.get_token() 
        if self.token.recognized_string == "=":
            self.expression_list.append(self.token.recognized_string)
            self.token= self.get_token()
            if self.token.recognized_string == "int":
                self.token= self.get_token()
                if self.token.recognized_string == "(":
                    self.token= self.get_token()
                    if self.token.recognized_string == "input":
                        quad=self.inter.genquad("in","_","_",inp)
                        self.inter.add_to_list(quad)
                        self.token= self.get_token()
                        if self.token.recognized_string == "(":
                            self.token= self.get_token()
                            if self.token.recognized_string == ")":
                                self.token= self.get_token()
                                if self.token.recognized_string == ")":
                                    self.token= self.get_token()
                                    self.expression_list.clear()
                                else:
                                    self.error('Expected: ")" to end declaration of embedded function "int()"')
                            else:
                                self.error('Expected: ")" to end declaration of embedded function "input()"')
                        else:
                            self.error('Declaration of embedded function "input()" expects "("')
                    else:
                        self.error('"int()" must contain keyword "input()"')
                else:
                    self.error('Declaration of embedded function "int()" expects "("')
            else:
                self.expression()  
                
                self.inter.expr_to_quad(self.expression_list,self.symbol_table)
                self.expression_list.clear()    
            
        else:
            self.error('Expected assignment operator "=" for declaring variable')
        

    def print_stat(self):
        if self.token.recognized_string == "(":
            self.token= self.get_token()
            self.expression()
            
            
            self.inter.expr_to_quad(self.expression_list,self.symbol_table)
            
            quad=self.inter.genquad("out",self.inter.ret,"_","_")
            
            self.inter.add_to_list(quad)
            self.inter.ret=""
            self.expression_list.clear()
            

            if self.token.recognized_string == ")":
                self.token= self.get_token()
            else:
                self.error('Expected: ")" to end declaration of embedded function "print()"')
        else:
            self.error('Declaration of embedded function "print()" expects "("')

    def return_stat(self):
        self.expression()

        self.inter.expr_to_quad(self.expression_list,self.symbol_table)
            
        quad=self.inter.genquad("ret",self.inter.ret,"_","_")

        self.inter.add_to_list(quad)
        self.inter.ret=""
        self.expression_list.clear()
        

    def if_stat(self):
        
        if self.token.family == Special_words().family_type[0] :
            self.condition()
            
            self.expression_list.clear()
        elif self.token.recognized_string == "(":
            self.token = self.get_token()
            self.condition()
            
            self.expression_list.clear()
            if self.token.recognized_string == ")":
                self.token = self.get_token()
            else:
                self.error('Expected: ")" to end declaration of keyword "if"')
        else:
            self.error('illegal if statement')
         
        if self.token.recognized_string == ":":
            self.token = self.get_token()
               
            if self.token.recognized_string == "#{":
                self.token = self.get_token()
                self.statements()
                if self.token.recognized_string == "#}":
                    self.token = self.get_token()
                else:
                    self.error('Expected: "#}" after statements of keyword "if"')
                
            else:
                self.statement()
            number_of_variables=len(self.inter.change_list)
            i=int(self.inter.nextquad())-1
            if self.token.recognized_string=="elif":
                self.inter.add_to_list(self.inter.genquad("jump","_","_","_"))
                
               
                self.elif_stat(number_of_variables)
                
                self.inter.change_list.append(i-99)
                
                i=int(self.inter.nextquad())-1
                self.inter.add_to_list(self.inter.genquad("jump","_","_","_"))
                self.inter.change_list.append(i-99)
                for i in range(number_of_variables):
                    self.inter.backpatch_false_list(str(int(self.inter.nextquad())+1))
                    
            if self.token.recognized_string=="else":
                for i in range(number_of_variables):
                    self.inter.backpatch_false_list(self.inter.nextquad())
                    
                self.else_stat()

            


    def elif_stat(self,number_of_variables):
 
        while self.token.recognized_string=="elif":
            
            self.token = self.get_token()
            for i in range(number_of_variables):
                self.inter.backpatch_false_list(self.inter.nextquad())
        
            if self.token.family == Special_words().family_type[0] :
                
                self.condition()
                self.expression_list.clear()
                
            elif self.token.recognized_string == "(":
                self.token = self.get_token()
                self.condition()
                
                self.expression_list.clear()
                if self.token.recognized_string == ")":
                    self.token = self.get_token()
                else:
                    self.error('Expected: ")" to end declaration of keyword "if"')
            else:
                self.error('illegal if statement')
            if self.token.recognized_string == ":":
                self.token = self.get_token()
                if self.token.recognized_string == "#{":
                    self.token = self.get_token()
                    self.statements()
                    if self.token.recognized_string == "#}":
                        self.token = self.get_token()
                    else:
                        self.error('Expected: "#}" after statements of keyword "if"')
                else:
                    self.statement()
        
        
        
        
    
    def else_stat(self):
        if self.token.recognized_string == "else":
            self.token = self.get_token()
            if self.token.recognized_string == ":":
                self.token = self.get_token()
                if self.token.recognized_string == "#{":
                    self.token = self.get_token()
                    self.statements()
                    if self.token.recognized_string == "#}":
                        self.token = self.get_token()     
                    else:
                        self.error('Expected: "#}" after statements of keyword "else"')     
                else:
                    self.statement() 
            else:
                self.error('Expected: ":" to end declaration of keyword "else"')
        
        


    def while_stat(self):
        condition_jump_counter=self.inter.nextquad()
        if self.token.family == Special_words().family_type[0]:
            self.condition()
            self.expression_list.clear()
        elif self.token.recognized_string == "(":
            self.token= self.get_token()
            self.condition()
            self.expression_list.clear()
            if self.token.recognized_string == ")":
                self.token= self.get_token()
            else:
                self.error('Expected: ")" to end declaration of keyword "while"')
        else:
            self.error('illegal while statement"')
            
        if self.token.recognized_string == ":":
            self.token= self.get_token()
            if self.token.recognized_string == "#{": 
                self.token = self.get_token()
                self.statements()
                self.inter.add_to_list(self.inter.genquad("jump","_","_",condition_jump_counter))
                if self.token.recognized_string == "#}":
                    self.token = self.get_token()

                else:
                    self.error('Expected: "#}" after statements of keyword "while"')
            else:
                self.statement() 
        num_of_variables=len(self.inter.change_list)
                            
        for i in range(num_of_variables):
            self.inter.backpatch_false_list(self.inter.nextquad())
        
            
       

    def id_list(self,str):
        if self.token.family == Special_words().family_type[0]:
            
            if str=="#int":
                var=Variable(self.token.recognized_string, "integer", self.symbol_table.offsets[len(self.symbol_table.table)-1])
                self.symbol_table.add_rec(var)
            elif str=="function":
                par=Parameter(self.token.recognized_string, "integer", "cv", self.symbol_table.offsets[len(self.symbol_table.table)-1])
                f_par=Formal_Parameter(self.token.recognized_string,"integer","cv")
                self.symbol_table.formal_par_list.append(f_par)
                
                self.symbol_table.add_rec(par)
            
            self.token= self.get_token()
            while self.token.recognized_string == ",":
                self.token= self.get_token()
                
                self.id_list(str)
        
    def expression(self):
        
        self.optional_sign()
        self.term()
        while self.token.recognized_string == "+" or self.token.recognized_string == "-":
            self.expression_list.append(self.token.recognized_string)
            
            self.token= self.get_token()
            self.term()

    def term(self):
        self.factor()
        while self.token.recognized_string == "*" or self.token.recognized_string =="//" or self.token.recognized_string=="%":
            self.expression_list.append(self.token.recognized_string)
            self.token= self.get_token()
            self.factor()

    def factor(self):
        if self.token.family == Special_words().family_type[2]:
            if(int(self.token.recognized_string)>32767 or int(self.token.recognized_string)<-32767):
                self.error('Int "'+self.token.recognized_string+'" out of bounds')
            
            self.expression_list.append(self.token.recognized_string)    
            self.token = self.get_token()
            
        elif self.token.recognized_string == "(":
            self.expression_list.append(self.token.recognized_string)
            self.token=self.get_token() 
            self.expression()
            if self.token.recognized_string == ")":
                self.expression_list.append(self.token.recognized_string)
                self.token = self.get_token()
            else:
                self.error('Illegal math operation: Expected ")"')
        elif self.token.family == Special_words().family_type[0]:
            if self.token.recognized_string in self.function_names:
                temp_list=[]
                while self.token.recognized_string != ")":
                    temp_list.append(self.token.recognized_string)
                    self.token=self.get_token()
                self.token=self.get_token()
                self.expression_list.append(self.inter.call_function(temp_list,self.symbol_table))
                
            else:
                self.expression_list.append(self.token.recognized_string)
                self.token = self.get_token()
                self.idtail()
        else:
            self.error('Math operation not possible between non numeric values')

    def idtail(self):
        if self.token.recognized_string == "(":
            self.expression_list.append(self.token.recognized_string)
            self.token= self.get_token()
            self.actual_par_list()
            if self.token.recognized_string == ")":
                self.expression_list.append(self.token.recognized_string)
                self.token= self.get_token()
            else:
                self.error('Expected ")" after function parameters')

    def actual_par_list(self):
        self.expression()
        while self.token.recognized_string == ",":
            self.expression_list.append(self.token.recognized_string)
            self.token= self.get_token()
            self.expression()

    def optional_sign(self):
        if self.token.recognized_string == "+":
            self.expression_list.append(self.token.recognized_string)
            self.token= self.get_token()
        elif self.token.recognized_string == "-":
            temp_num=self.token.recognized_string
            self.token= self.get_token()
            temp_num+=self.token.recognized_string
            self.expression_list.append(temp_num)
            
            
        
        
    def condition(self):
        self.bool_term()
        while self.token.recognized_string == "or":
            self.expression_list.append(self.token.recognized_string)
            self.token= self.get_token()
            self.bool_term()


    def bool_term(self):
        self.bool_factor()
        while self.token.recognized_string == "and":
            self.expression_list.append(self.token.recognized_string)
            self.token= self.get_token()
            self.bool_factor()


    def bool_factor(self):
        if self.token.recognized_string == "not":
            self.expression_list.append(self.token.recognized_string)
            self.token= self.get_token()
            if self.token.recognized_string == "(":
                self.expression_list.append(self.token.recognized_string)
                self.token= self.get_token()
                self.condition()
                if self.token.recognized_string == ")":
                    self.expression_list.append(self.token.recognized_string)
                    self.token= self.get_token()
                else:
                    self.error('Parenthesis never closed: Expected ")"')
        elif self.token.recognized_string == "(":
            self.expression_list.append(self.token.recognized_string)
            self.token= self.get_token()      
            self.condition()
            if self.token.recognized_string == ")":
                self.expression_list.append(self.token.recognized_string)
                self.token= self.get_token() 
            else:
                self.error('Parenthesis never closed: Expected ")"')
        else:
            self.expression()
            if self.token.family == Special_words().family_type[4]:#rel operator
                self.expression_list.append(self.token.recognized_string)
                self.token= self.get_token()
                self.expression()
                
                while(self.token.family == Special_words().family_type[5]):
                    self.expression_list.append(self.token.recognized_string)
                    self.token= self.get_token()
                    self.expression()
                    self.expression_list.append(self.token.recognized_string)
                    self.token= self.get_token()
                    self.expression()
                    
                self.inter.expr_to_quad(self.expression_list,self.symbol_table)
              
            else:
                self.error('Relation operator "'+self.token.recognized_string+'" does not exist')


        

class Inter_Code:

    def __init__(self):
        self.t_counter = 0
        self.line=99
        self.quad_list=[self.genquad("jump","_","_","_")]
        
        self.main_name=""
        
        self.true_list=[]
        self.false_list=[]
        self.change_list=[]
        self.ret=""
        self.condition_jump_counter=0
        self.temp_variables_list=[]
    
    def nextquad(self):
        return str(self.line+1)
    
    def genquad(self,op,x,y,z):
        self.line+=1
        return [op,x,y,z]

    def newtemp(self):
        t = "T$" + str(self.t_counter)
        self.t_counter+=1
        self.temp_variables_list.append(t)
        return t

    def emptylist(self):
        return ["_","_","_","_"]
    
    def makelist(self,x):
        temp_list= x
        return temp_list

    def mergelist(self,list1,list2):
        x=list1+list2
        return x

    def backpatch(self,list,next_label):
        list.pop()
        list.append(next_label)
 
    
    def add_to_list(self,quad):
        self.quad_list.append(quad)
       
   

    def __expr_to_quad(self,list,symbol_table):  
        i=0
        while i<len(list):
            if list[i]=="*" or list[i]=="//":
                temp=self.newtemp()
                t=TemporaryVariable(temp,"integer",symbol_table.offsets[len(symbol_table.table)-1])
                symbol_table.add_rec(t)

                quad=self.genquad(list[i],list[i-1],list[i+1],temp)
               
                self.add_to_list(quad)
                list[i]=temp
                list.pop(i+1)
                list.pop(i-1)
            else:   
                i+=1

        i=0
        while i<len(list):  
            if list[i]=="+" or list[i]=="-":
                temp=self.newtemp()
                t=TemporaryVariable(temp,"integer",symbol_table.offsets[len(symbol_table.table)-1])
                symbol_table.add_rec(t)

                quad=self.genquad(list[i],list[i-1],list[i+1],temp)
             
                self.add_to_list(quad)
                list[i]=temp
                list.pop(i+1)
                list.pop(i-1)
            else:   
                i+=1
        return list
            
    def expr_to_quad(self,list,symbol_table):
        flag=False
        temp_list=[]
        temp_list2=list
        if len(list)==0:
            return
        if len(list)==1:
            
            self.ret=list[0]
            return
        
        if "(" in list and ")" in list:
            for i in range(len(list)):
                if list[i]=="(":
                    flag=True
                    list[i]=""
                elif list[i]==")":
                    flag=False
                    list[i]=self.__expr_to_quad(temp_list,symbol_table)[0]
                elif flag:
                    temp_list.append(list[i])
                    list[i]=""

        list= [value for value in list if value != ""]
        list=self.__expr_to_quad(list,symbol_table)
        
        if temp_list2[1]!="=" and temp_list2[1] not in Special_words().rel_operators:
            temp=self.newtemp()
            list.insert(0,temp)
            self.ret=list[0]
            list.insert(1,"=")
            t=TemporaryVariable(temp,"integer",symbol_table.offsets[len(symbol_table.table)-1])
            symbol_table.add_rec(t)

        if(list[1] not in Special_words().rel_operators):
            quad=self.genquad(list[1],list[2],"_",list[0])
      
            self.add_to_list(quad)
        else:
            self.cond_to_quad(list)
            
        
    def __cond_to_quad(self,list,is_not):
        if is_not:
            if list[1]=="==":
                list[1]="!="
            elif list[1]=="!=":
                list[1]="=="

            elif list[1]=="<":
                list[1]=">="

            elif list[1]==">=":
                list[1]=["<"]

            elif list[1]==">":
                list[1]="<="

            elif list[1]=="<=":
                list[1][">"]

        true_quad=self.genquad(list[1],list[0],list[2],"_")
        false_quad=self.genquad("jump","_","_","_")
        self.condition_jump_counter=int(self.nextquad())-1
        
        self.true_list.append(true_quad)
        self.false_list.append(false_quad)
        
    def cond_to_quad(self, list):
        temp_list=[]
        is_not=False
        i=0  
        
        while len(list)>i:
            
            if list[i]=="not" or list[i]=="(":
                is_not=True
            else:
                temp_list.append(list[i])
                
            
            if len(temp_list)==3:
                i+=1
               
                if(len(list)==i):
                    self.__cond_to_quad(temp_list,is_not)
                    self.backpatch(self.true_list[len(self.true_list)-1],self.nextquad())
                    
                    
                    break
                
                self.__cond_to_quad(temp_list,is_not)
                
                if list[i]==")":
                    is_not=False
                    i+=1
                
                if list[i]=="or" :
                    self.backpatch(self.false_list[len(self.false_list)-1],self.nextquad())
                    self.backpatch(self.true_list[len(self.true_list)-1],"or")   
                elif list[i]=="and":
                    
                    self.backpatch(self.true_list[len(self.true_list)-1],self.nextquad())
                    
                temp_list.clear()  
                
            i+=1
        i=0
        
        
        for true in self.true_list:
            if(true==self.true_list[len(self.true_list)-1]):
                break
            
            if(true[3]=="or"):
                self.backpatch(true, self.true_list[len(self.true_list)-1][3])
            
            self.add_to_list(true)
            self.add_to_list(self.false_list[i])
            self.change_list.append(len(self.quad_list)-1)
            
            i+=1
        
        self.add_to_list(self.true_list.pop())
        self.add_to_list(self.false_list[i])
        
        self.change_list.append(len(self.quad_list)-1)
        
        self.true_list.clear()
        
            
    def begin_block(self, function_name):
        quad=self.genquad("begin_block",function_name,"_","_")
   
        self.add_to_list(quad)
    
    def end_block(self,function_name):
        quad=self.genquad("end_block",function_name,"_","_")

        self.add_to_list(quad)
    
    def create_inter_file(self):
        f = open("inter_code.int", "w")
        
        self.backpatch(self.quad_list[0],self.main_name)
        
        line=100
        for quad in self.quad_list:   
            
            f.write(str(line)+": "+quad[0]+", "+quad[1]+", "+quad[2]+ ", "+quad[3]+"\n")
            line+=1
        f.close()

    def backpatch_false_list(self,where_to_go):
       
        i=self.change_list.pop()
        self.quad_list.pop(i)
        self.quad_list.insert(i,["jump","_","_",where_to_go])

    def call_function(self,list,symbol_table):
        function_name=list[0]
        list.pop(0)
        list.pop(0)
       
        temp_lst=[]
        if "," in list:
            for parameter in list:
                if parameter==",":
                    if len(temp_lst)==1:
                        self.add_to_list(self.genquad("par",temp_lst[0]," CV",function_name))
                        temp_lst.clear()
                    else:
                        self.expr_to_quad(temp_lst,symbol_table)
                        par=self.quad_list[len(self.quad_list)-1][3]
                        self.add_to_list(self.genquad("par",par,"CV",function_name))
                        temp_lst.clear()  
                else:   
                    temp_lst.append(parameter)
            if len(temp_lst)==1:
                self.add_to_list(self.genquad("par",temp_lst[0]," CV",function_name))
                temp_lst.clear()
            else:
                self.expr_to_quad(temp_lst,symbol_table)
                par=self.quad_list[len(self.quad_list)-1][3]
                self.add_to_list(self.genquad("par",par," CV",function_name))
            
        elif len(list)==1:
            if list[0].isnumeric():
                self.expr_to_quad(temp_lst,symbol_table)
                par=self.quad_list[len(self.quad_list)-1][3]
                self.add_to_list(self.genquad("par",par," CV",function_name))
            else:
                self.add_to_list(self.genquad("par",list[0]," CV",function_name))
        elif len(list)==0:
            pass
        else:
            for parameter in list: 
                temp_lst.append(parameter)
            self.expr_to_quad(temp_lst,symbol_table)
            par=self.quad_list[len(self.quad_list)-1][3]
            self.add_to_list(self.genquad("par",par," CV",function_name))  

        temp=self.newtemp()
        self.add_to_list(self.genquad("par",temp," RET",function_name))
        self.add_to_list(self.genquad("call","_","_",function_name))
        
        t=TemporaryVariable(temp,"integer",symbol_table.offsets[len(symbol_table.table)-1])
        symbol_table.add_rec(t)

        return temp

        
 
class Table:

    def __init__(self):
        self.table=[[0]]
        
        self.offsets=[12]
        self.formal_par_list=[]
        f = open("symbol_table.sym", "w")
        f.close()
        
        
    def add_rec(self, rec):
        for list in self.table:
            for record in list:
                if type(rec)!=str and type(rec)!=int and type(record)!=str and type(record)!=int:
                    if record.name==rec.name:
                        return
        
        self.table[len(self.table)-1].append(rec)
        
        if type(rec)!=Function:
            self.offsets[len(self.table)-1]+=4
        

    def add_level(self):
        #self.print_level()
        
        self.offsets.append(12)
        
        temp_list=[]
        temp_list.append(len(self.table))
        self.table.append(temp_list)
        

    def get_current_level(self):
        return len(self.table)-1
       
    def create_symbol_table_file(self):
        f = open("symbol_table.sym", "a")
        f.write("\n")
        for list in self.table:
            for rec in list:
                if type(rec)==str:
                    f.write(rec+"|")
                elif type(rec)==int:
                    f.write(" ("+str(rec)+") ")
                else:
                    f.write(rec.get_info())
        f.close()
    
         
    def remove_level(self):
        #self.print_level()
        self.create_symbol_table_file()
        length=len(self.table)-1
        

        self.table[length].pop()
        self.table.pop()
        self.offsets.pop()
        

    def print_level(self):
        for list in self.table:
            for rec in list:
                if type(rec)==str:
                    print(rec,end="|")
                elif type(rec)==int:
                    print(" ("+str(rec),end=") ")
                else:
                    rec.print_()
        print()


    def update_formal_parameters(self,name, formal_par):#for functions only
        for list in self.table:
            for rec in list:
                if type(rec)==Function:
                    if rec.name==name:
                        rec.formalParameters.append(formal_par)
                        return
                    

    def update_starting_quad(self,name,starting_quad):
        for list in self.table:
            for rec in list:
                if type(rec)==Function:
                    if rec.name==name:
                        rec.startingQuad=starting_quad
                        return
                    
    def update_frameLength(self,name,frameLength):
        for list in self.table:
            for rec in list:
                if type(rec)==Function:
                    if rec.name==name:
                        rec.framelength=frameLength
                        
                        return

    


    def find_rec_offset(self,rec):
        counter=len(self.table)-1
        for level in reversed(self.table):
            for record in level:
                if type(rec)!=int and type(record)!=str and type(record)!=int and type(rec)!= Function and type(record)!=Function:
                    if record.name==rec:
                        return [record,counter]
            counter-=1

    def find_func_framelength(self,name):
        for list in self.table:
            for rec in list:
                if type(rec)==Function:
                    if rec.name==name:
                        return rec.framelength


    def count_function_formal_par(self,name):
        for list in self.table:
            for rec in list:
                if type(rec)==Function:
                    if rec.name==name :
                        return len(rec.formalParameters)
                    
    def find_rec(self,rec):
        counter=len(self.table)-1
        for level in reversed(self.table):
            for record in level:
                if type(rec)!=int and type(record)!=str and type(record)!=int and type(rec)!= Function and type(record)!=Function:
                    if record.name==rec:
                        
                        return [record,counter]
            counter-=1
            
    def find_tempVar(self,rec):
        counter=len(self.table)-1
        
        for level in reversed(self.table):
            
            for record in level:
                
                if type(rec)==str and type(record)==TemporaryVariable :
                    
                    if record.name==rec : 
                        
                        return [record,counter]
            counter-=1        
    
    
class Variable:
    def __init__(self,name,datatype,offset):
        self.name=name
        self.datatype=datatype
        self.offset=offset
    
    def print_(self):
        print(self.name,self.datatype,self.offset," | ")
        
    def get_info(self):
        ret_str = str(self.name)+" "+str(self.datatype)+" "+str(self.offset)+" | "
        return ret_str

        
class TemporaryVariable:
    def __init__(self,name,datatype,offset):
        self.name=name
        self.datatype=datatype
        self.offset=offset

    def print_(self):
        print(self.name,self.datatype,self.offset,end=" | ")
        
    def get_info(self):
        ret_str = str(self.name)+" "+str(self.datatype)+" "+str(self.offset)+" | "
        return ret_str

class Parameter:
    def __init__(self,name,datatype,mode,offset):
        self.name=name
        self.datatype=datatype
        self.mode=mode
        self.offset=offset

    def print_(self):
        print(self.name,self.datatype,self.mode,self.offset,end=" | ")
        
    def get_info(self):
        ret_str = str(self.name)+" "+str(self.datatype)+" "+str(self.mode)+" "+str(self.offset)+" | "
        return ret_str

class Formal_Parameter:
    def __init__(self,name,datatype,mode):
        self.name=name
        self.datatype=datatype
        self.mode=mode

    def print_(self):
        print(self.name,self.datatype,self.mode,end=" | ")
    
    def get_info(self):
        ret_str = str(self.name)+" "+str(self.datatype)+" "+str(self.mode)+" | "
        return ret_str

class Function:
    def __init__(self,name,datatype,startingQuad,framelength):
        self.name=name
        self.datatype=datatype
        self.startingQuad=startingQuad
        self.framelength=framelength
        self.formalParameters=[]
    
    def print_(self):
        print(self.name,end=" | ")
        
    def get_info(self):
        ret_str = str(self.name)+" | "
        return ret_str




class FinalCode :
    

    def __init__(self,table,temp_variable_list):
        self.final_code_list=[".data",'str_nl: .asciz "\\n"',".text\n"]
        self.symbol_table = table
        self.l_counter=100
        self.formal_par_count=1
        self.function_label_dic={}
        self.temp_variable_list=temp_variable_list

    def label_maker(self):
        l = "L_" + str(self.l_counter)+ ":"
        self.l_counter+=1
        return l
    
    def produce(self,str):
        self.final_code_list.append(str) 

    def create_assembly_file(self):
        f = open("ascode.asm", "w")
        for line in self.final_code_list:   
            f.write(str(line)+"\n")
        f.close()

    def gnlvcode(self, entity,level):
        
        
        t = 1
        self.produce("lw t0,-4(sp) ")
        while (t < (abs(int(self.symbol_table.get_current_level()) - int(level)))) :
            self.produce("lw t0,-4(t0) ")
            t += 1 
        self.produce("addi t0, t0," + "-" + str(entity.offset))



    def loadvr(self, variable, register) :
        
        if (variable.isdigit()) :
            self.produce("li " + register + ", " + variable )
        else :
            
            res = self.symbol_table.find_rec(variable)
            entity = res[0]
            level = res[1]
            if level == self.symbol_table.get_current_level() :
                self.produce("lw " + register + ",-" + str(entity.offset) + "(sp)")
            elif ((level != self.symbol_table.get_current_level()) and (type(entity) =="Parameter:" or type(entity) == "Variable:")):
                self.gnlvcode(entity,level)
                self.produce("lw " + register + ",(t0)")
            elif level == 0 :
                self.produce("lw " + register + ",-" + str(entity.offset) +"(gp)")
        

    def storerv(self, register, variable) :
        
        if(variable in self.temp_variable_list):
            res = self.symbol_table.find_tempVar(variable)
            
            entity=res[0]
            level=res[1]
        else:
            res = self.symbol_table.find_rec(variable)
            entity = res[0]
            level = res[1]
            
        if level == self.symbol_table.get_current_level() :
            
            self.produce("sw " + register + ",-" + str(entity.offset) + "(sp)")
        elif level == 0 :
            self.produce("sw " + register + ",-" + str(entity.offset) +"(gp)")
        else :         
            self.gnlvcode(entity,level)
            self.produce("sw t0,-" + str(entity.offset) + "(sp)")
            
            
    def createFinalCode(self,list, main_name,start_line):
        d=0
        i=start_line
        while i<len(list):
            
            quad_operator=list[i][0]
            l=self.label_maker()
            self.produce(l)
            
            
            if quad_operator=="begin_block":
                
                if list[i][1]==main_name:
                    self.formal_par_count=1
                    
                    l_main="L_" +main_name
                    
                    self.final_code_list.insert(4,"j "+l_main)

                    self.produce(l_main+ ":")
                    
                    self.produce("#"+str(self.l_counter-1) +": begin_block, "+list[i][1]+", _, _")#adds comment to show quad translated
                    
                    self.produce("addi sp, sp, "+str(self.symbol_table.offsets[0]))
                    
                    self.produce("mv s0 sp")
                    
                else:
                    

                    self.produce("#"+str(self.l_counter-1) +": begin_block, "+list[i][1]+", _, _")#adds comment to show quad translated
                    self.function_label_dic.update({list[i][1]:l[:-1]})
                self.produce("sw ra,(sp)")
                    
                    
                    
            elif quad_operator=="end_block":
                
                self.produce("#"+str(self.l_counter-1) +": end_block, "+list[i][1]+", _, _")#adds comment to show quad translated
                self.produce("lw ra,(sp)")
                self.produce("jr ra")
                
            elif quad_operator=="halt":
                self.produce("#"+str(self.l_counter-1) +": halt, _, _, _")#adds comment to show quad translated
                self.produce("li a0, 0")
                self.produce("li a7, 93")
                self.produce("ecall")
                
            elif quad_operator=="ret":
                self.produce("#"+str(self.l_counter-1) +": ret, "+list[i][1]+", _, _")#adds comment to show quad translated
                
                    
                self.produce("lw t0,-8(sp)")
                self.loadvr(list[i][1], "t1")
                self.produce("sw t1,(t0)")
                self.produce("lw ra, (sp)")
                self.produce("jr ra")
                
                           
            elif quad_operator== "par":     
                self.produce("#"+str(self.l_counter-1) +": par, "+list[i][1]+","+ list[i][2]+", _")#adds comment to show quad translated
                framelength=self.symbol_table.find_func_framelength(list[i][3])
                
                
                offset_1=self.symbol_table.find_rec_offset(list[i][1])
                if self.formal_par_count==1:
                    self.produce("addi fp, sp, "+str(framelength))
                    
                
                
                elif list[i][2]==" CV":
                    print(list[i],self.formal_par_count)
                    self.loadvr(list[i][1], "t1")

                    self.produce("sw t1, -"+str(12+self.formal_par_count*4) +"(fp)")
                    
                    self.formal_par_count+=1
                elif list[i][2]==" RET":
                    self.produce("addi t0, sp, -"+str(offset_1[0]))
                    self.produce("sw t0, -8(fp)")
                    self.formal_par_count=1
                    
                 
            elif quad_operator=="call":
                self.produce("#"+str(self.l_counter-1) +": call, _, _, "+list[i][3])#adds comment to show quad translated
                self.produce("sw sp , -4(fp)")
                
                self.produce("addi sp, sp, "+str(framelength))
                
                function_label=self.function_label_dic.get(list[i][3])
                
                self.produce("jal "+function_label)
                self.produce("addi sp, sp, -"+str(framelength))

            elif quad_operator=="in":
                self.produce("#"+str(self.l_counter-1) +": input, _, _, "+list[i][3])#adds comment to show quad translated
                self.produce("li a7, 5")
                self.produce("ecall")
                self.storerv("a0",list[i][3])
                
            elif quad_operator=="out":
                self.produce("#"+str(self.l_counter-1) +": print, "+list[i][1]+", _, _")#adds comment to show quad translated
                self.loadvr(list[i][1], "a0")
                self.produce("li a7,1")
                self.produce("ecall")
                self.produce("la a0,str_nl")
                self.produce("li a7,4")
                self.produce("ecall")
            
            elif quad_operator=="jump":
                if list[i][3]!="_":
                    self.produce("#"+str(self.l_counter-1) +": jump , _, _, "+list[i][3])#adds comment to show quad translated
                    self.produce("j L_"+list[i][3])
     
            elif quad_operator== "=":
                self.produce("#"+str(self.l_counter-1) +": =, "+ str(list[i][1])+", _, "+list[i][3])#adds comment to show quad translated
                self.loadvr(list[i][1], "t1")
                self.storerv("t1", list[i][3])
                        
                    
            elif quad_operator in Special_words().math_operators:
                self.produce("#"+str(self.l_counter-1) +": "+quad_operator+", "+ str(list[i][1])+", "+list[i][2]+", "+list[i][3])#adds comment to show quad translated
                
                self.loadvr(list[i][1], "t1")
                self.loadvr(list[i][2], "t2")
                        
                if quad_operator=="+":
                    oper="add"
                elif quad_operator=="-":
                    oper="sub"    
                elif quad_operator=="*":
                    oper="mul"
                    
                elif quad_operator=="//":
                    oper="div"
                    
                self.produce(oper + " t1,t1,t2")
                
                self.storerv("t1" ,list[i][3])  
                    
            elif quad_operator in Special_words().rel_operators:
                self.produce("#"+str(self.l_counter-1) +": "+quad_operator+", "+ list[i][1]+", "+list[i][2]+", "+list[i][3])#adds comment to show quad translated
                self.loadvr(list[i][1], "t1")
                
                self.loadvr(list[i][2], "t2")
                
                if quad_operator== "==":
                    oper="beq"
                elif quad_operator=="<=":
                    oper="ble"
                elif quad_operator== "<":
                    oper="blt"
                elif quad_operator==">=":
                    oper="bge"  
                elif quad_operator== ">":
                    oper="bgt"
                elif quad_operator=="!=":
                    oper="bne"
                self.produce(oper+", t1, t2, L_"+list[i][3])  
            
            i+=1  
        return i 
if __name__ == '__main__':
    file_name=sys.argv[1]
    phase1=Syntax(file_name)
    phase1.start_rule()
    print("Compilation Done")