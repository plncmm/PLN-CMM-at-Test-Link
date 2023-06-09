import random 

def split_dataset(path, train_size, val_size, test_size):
    with open(path) as f:
        data = f.read()
    
    sentences = data.split("\n\n")[:-1]

    random.shuffle(sentences)
    n_train = int(len(sentences) * train_size)
    n_val = int(len(sentences) * val_size)

    train_file = open("train.iob2", "w")
    for sent in sentences[:n_train]:
        train_file.write(sent)
        train_file.write("\n\n")
    train_file.close()

    dev_file = open("val.iob2", "w")
    for sent in sentences[n_train : n_train + n_val]:
        dev_file.write(sent)
        dev_file.write("\n\n")
    dev_file.close()

    test_file = open("test.iob2", "w")
    for sent in sentences[n_train + n_val :]:
        test_file.write(sent)
        test_file.write("\n\n")
    test_file.close()
    
    

if __name__=='__main__':
    d = {}
    f = open('TESTLINK_training_data/training.txt','r').read()
    examples = f.split('\n\n')
    print('Total de ejemplos: ' + str(len(examples)))
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
    

    output = open('ner.iob2', 'w')

    for i, (id, data) in enumerate(d.items()):
        total_entities = 0
        tokenized_file = open(f'training_tokenized/{id}.tsv').read()
        relations = data['relations']
        for sentence in tokenized_file.split('\n\n'):
            for line in sentence.splitlines():
                info = line.split()[1:]
                start_index = int(info[0].split('-')[0])
                end_index = int(info[0].split('-')[1])
                token = info[1]
                label = 'O'

                for r in relations:
                    
                    head_entity = r[0]
                    tail_entity = r[1]
                    head_start_index = int(head_entity[0])
                    head_end_index = int(head_entity[1])
                    tail_start_index = int(tail_entity[0])
                    tail_end_index = int(tail_entity[1])

                    if start_index==head_start_index and end_index<=head_end_index:
                        label='B-PROCEDURE'
                    
                    elif start_index>head_start_index and end_index<=head_end_index:
                        label='I-PROCEDURE'
                    
                    if start_index==tail_start_index and end_index<=tail_end_index:
                        label='B-RESULT'
                    
                    elif start_index>tail_start_index and end_index<=tail_end_index:
                        label='I-RESULT'

                
                output.write(f'{token} {label}\n')   
               
            output.write('\n')
    output.close()

    split_dataset('ner.iob2', train_size=0.6, val_size=0.2, test_size=0.2)

        