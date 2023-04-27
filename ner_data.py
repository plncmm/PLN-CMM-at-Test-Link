from collections import defaultdict


def create_re_format(sentences, relations, path):
    out = open(path, 'w')
    
    count = 1

    for i, (sent, rel) in enumerate(zip(sentences, relations)):
        
        tokens = [line.split()[0] for line in sent.splitlines()]
        out.write('# global.columns = id form ner\n')
        out.write(f"# text = {' '.join(tokens)}\n")
        out.write(f"# sentence_id = {count}\n")
        
        already_added = False
        s = ""
        for k, v in rel.items():

            if already_added:
                s+='|'
            
            s+=f"{v[0].split('-')[1]};{v[1].split('-')[1]};{v[2].split('-')[1]};{v[3].split('-')[1]};RESULT_OF"
            already_added=True

        if already_added:
            out.write(f"# relations = {s}\n")

        for k, line in enumerate(sent.splitlines()):
            token = line.split()[0]
            label = line.split()[1]
            out.write(f"{k+1} {token} {label}\n")
        count+=1



        


        out.write("\n")
        

if __name__=='__main__':
    
    d = {}
    f = open('TESTLINK_training_data/training.txt','r').read()
    examples = f.split('\n\n')
    for example in examples:
        id = example.split('|')[0]
        relations = []
        for line in example.split('|')[2].splitlines():
            if line.startswith(id):
                info = line.split('\t')
                tail_start = info[2].split('-')[0]
                tail_end = info[2].split('-')[1]
                head_start = info[3].split('-')[0]
                head_end = info[3].split('-')[1]
                tail_entity = info[4]
                head_entity = info[5]
                relations.append([[head_start, head_end, head_entity], [tail_start, tail_end, tail_entity]])
            else:
                text = line
        d[id] = {'text': text, 'relations': relations}


    from collections import defaultdict

    sentence_relations = []
    output = open('ner_re.conll', 'w')
    for i, (id, data) in enumerate(d.items()):
        total_entities = 0
        tokenized_file = open(f'training_tokenized/{id}.tsv').read()
        relations = data['relations']
        for sentence in tokenized_file.split('\n\n'):
       

            res = defaultdict(list)
            for j, line in enumerate(sentence.splitlines()):
                info = line.split()[1:]
                start_index = int(info[0].split('-')[0])
                end_index = int(info[0].split('-')[1])
                token = info[1]
                label = ''
                
                for k, r in enumerate(relations):
                    
                    head_entity = r[0]
                    tail_entity = r[1]
                    head_start_index = int(head_entity[0])
                    head_end_index = int(head_entity[1])
                    tail_start_index = int(tail_entity[0])
                    tail_end_index = int(tail_entity[1])

                    if start_index==head_start_index:
                        res[k].append(f"Start Head-{j+1}")
                        label+= f"START_HEAD_{k} "
                    
                    if end_index==head_end_index:
                        res[k].append(f"End Head-{j+1}")
                 
                        label+= f"END_HEAD_{k} "

                    if start_index==tail_start_index:
                        res[k].append(f"Start Tail-{j+1}")
                      
                        label+= f"START_TAIL_{k} "
                    
                    if end_index==tail_end_index:
             
                        res[k].append(f"End Tail-{j+1}")
                        label+= f"END_TAIL_{k} "

                output.write(f'{token} {label}\n')   

            sentence_relations.append(res) 
            
            output.write('\n')
        
    output.close()



    f = open('ner.iob2', 'r').read()

    sentences = f.split('\n\n')

    n_train = int(len(sentences)*0.6)
    n_val = int(len(sentences)*0.2)
    
    create_re_format(sentences[0:n_train], sentence_relations[0:n_train], 'train.conllu')
    create_re_format(sentences[n_train:n_train+n_val], sentence_relations[n_train:n_train+n_val], 'val.conllu')
    create_re_format(sentences[n_train+n_val:], sentence_relations[n_train+n_val:], 'test.conllu')