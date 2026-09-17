DATA = {'source_sha': '2029eb28619471a28770fa03295fe77165999db9', 'sections': [{'heading': '2.1 视听广义零样本学习', 'paragraphs': ['视听广义零样本学习的核心，是借助类别语义将已见类的视听知识迁移至未见类。针对视听与文本之间的模态差异，Parida等[1]通过CJME构建共享嵌入空间，Mazumder等[2]在AVGZSLNet中引入标签特征重构，从几何对齐与语义保留两个角度增强跨模态对应关系。针对单一类别名称信息不足和特征表达受限的问题，Chen等[7]利用大语言模型生成细粒度描述，并以语义相似度调节训练间隔；Kurzendörfer等[4]则结合CLIP与CLAP的预训练特征及双文本嵌入，增强可迁移的视听—语义表示。', '除丰富语义内容外，类别原型的可分性同样影响识别效果。Mo与Morgado[10]在EZ-AVGZL中联合优化类别分离与语义关系保持，并以优化后的类别嵌入查询视听特征，建立非线性匹配。这说明类别语义不仅可以充当分类参照，也可以参与特征选择。', '因此，本文进一步关注类别语义如何引导局部判别证据的形成，而不局限于改进表示对齐与匹配函数。我们利用DSPO构建判别性语义参照，并将其与属性级描述共同用于SGTG的时序条件化，再以候选类别调节DMIF中的证据融合，使语义信息贯穿证据提取与识别决策。']}, {'heading': '2.2 音视频跨模态交互与融合', 'paragraphs': ['视听融合需要在利用模态互补性与抑制无关信息传播之间取得平衡。针对跨模态对应关系难以显式建模的问题，Mercea等[3]在AVCA中通过跨模态注意力交换视听信息；在更一般的多模态序列学习中，Tsai等[12]利用定向交叉注意力建模非对齐序列之间的依赖。这类方法强化了模态间的信息交换，但交互本身并不等同于对信息可靠性的筛选。', '围绕选择性交互，Nagrani等[14]通过少量瓶颈token限制跨模态信息流；Lin等[17]面向多模态情感分析，以掩码注意力分离模态内与模态间关系，并动态调节两者的贡献。进一步地，Ma等[36]在FAMAV中引入文本条件语义门控，对视听通道进行语义相关的选择。这些研究分别从交互容量、关系类型和语义条件三个角度，为减少无效信息交换提供了思路。', '为使融合决策与类别相关的时序证据相适应，本文将选择性交互与时序证据提取相结合。DMIF对SGTG增强后的序列分别建模模态内与模态间关系，并保留未经关系重组的直接时序证据；随后结合样本表征与候选类别原型，对三路证据进行归一化加权。由此，融合策略不仅取决于输入样本，也取决于当前待判别的类别及其可用证据。']}, {'heading': '2.3 时序建模与时序定位', 'paragraphs': ['时序建模不仅需要刻画片段间的依赖，还需要确定哪些片段支持当前语义目标。针对时间平均表征难以利用动态结构的问题，Mercea等[5]通过TCaF建模时序与跨模态关系。针对冗余片段干扰，Li等分别在PSTP-Net[19]和TSPM[20]中利用问题相关线索选择关键片段，将计算集中于更具判别性的内容；这类离散选择策略的证据覆盖仍受保留片段集合限制。', '为显式刻画目标相关片段的连续权重，Xiao等[22]在视觉定位问答中采用高斯掩码进行证据软定位；Kim等[23]进一步提出QA-TIGER，以问题为条件生成多个高斯专家，在音频和视觉时间轴上分别聚合相关证据。相较于离散筛选，这类方法通过参数化的时间权重表达证据的局部性，并允许多个片段共同支持预测。', '然而，问题条件化定位依赖逐样本给定的问句，其目标并非在已见与未见事件类别的联合空间中完成分类。为实现面向未见类别的时序证据提取，本文以候选类别的属性描述和判别性原型构建定位条件，将问题驱动的连续聚合转化为类别驱动的证据建模。SGTG输出保留时间结构的增强序列及直接证据摘要，并与后续解耦融合协同完成候选类别评分，而不依赖测试样本的问句或真实类别标签。']}], 'reference_updates': {'2': 'MAZUMDER P, SINGH P, PARIDA K K, et al. AVGZSLNet: audio-visual generalized zero-shot learning by reconstructing label features from multi-modal embeddings[C]//Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV). 2021: 3090-3099.', '7': 'CHEN H, LI Y, HONG Y, et al. Boosting audio-visual zero-shot learning with large language models[EB/OL]. arXiv:2311.12268, 2023 (v2, 2024). DOI: 10.48550/arXiv.2311.12268.', '10': 'MO S, MORGADO P. Audio-visual generalized zero-shot learning the easy way[C]//Proceedings of the European Conference on Computer Vision (ECCV). 2024: 377-395. DOI: 10.1007/978-3-031-73209-6_22.', '12': 'TSAI Y H H, BAI S, LIANG P P, et al. Multimodal transformer for unaligned multimodal language sequences[C]//Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL). 2019: 6558-6569. DOI: 10.18653/v1/P19-1656.', '14': 'NAGRANI A, YANG S, ARNAB A, et al. Attention bottlenecks for multimodal fusion[C]//Advances in Neural Information Processing Systems (NeurIPS). 2021, 34: 14200-14213.', '17': 'LIN J, WANG Y, XU Y, et al. Semi-IIN: semi-supervised intra-inter modal interaction learning network for multimodal sentiment analysis[C]//Proceedings of the AAAI Conference on Artificial Intelligence (AAAI). 2025, 39(2): 1411-1419. DOI: 10.1609/aaai.v39i2.32131.', '19': 'LI G, HOU W, HU D. Progressive spatio-temporal perception for audio-visual question answering[C]//Proceedings of the 31st ACM International Conference on Multimedia (ACM MM). 2023: 7808-7816. DOI: 10.1145/3581783.3612293.', '20': 'LI G, DU H, HU D. Boosting audio visual question answering via key semantic-aware cues[C]//Proceedings of the 32nd ACM International Conference on Multimedia (ACM MM). 2024: 5997-6005. DOI: 10.1145/3664647.3680803.', '23': 'KIM H, JUNG I, SUH D, et al. Question-aware Gaussian experts for audio-visual question answering[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 2025: 13681-13690.', '36': 'MA S, NIU X, TANG H, et al. Fusion-regularized alignment modality-adaptive audio-visual network for audio-visual zero-shot learning[J]. Neurocomputing, 2026, 685: 133693. DOI: 10.1016/j.neucom.2026.133693.'}}

import argparse, copy, hashlib, json, pathlib, re, zipfile
from lxml import etree as E

NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'm':'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'w14':'http://schemas.microsoft.com/office/word/2010/wordml'}
W='{'+NS['w']+'}'
CITE=re.compile(r'\[(\d+(?:\s*[,，–-]\s*\d+)*)\]')

def blobsha(data):
    return hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()

def txt(el):
    return ''.join(el.xpath('.//w:t/text()',namespaces=NS))

def paragraph_nodes(p):
    return [t for t in p.iter(W+'t') if next(t.iterancestors(W+'p')) is p]

def refnums(match):
    result=[]
    for item in re.split(r'[,，]',match[1]):
        ends=re.split(r'[-–]',item)
        result.extend(range(int(ends[0]),int(ends[1])+1) if len(ends)==2 else [int(ends[0])])
    return result

def replace_citations(p,mapping):
    nodes=paragraph_nodes(p)
    raw=''.join(t.text or '' for t in nodes)
    spans=[]; pos=0
    for t in nodes:
        length=len(t.text or ''); spans.append((t,pos,pos+length)); pos+=length
    count=0
    for match in reversed(list(CITE.finditer(raw))):
        repl='['+','.join(str(mapping[n]) for n in refnums(match))+']'
        if repl==match[0]: continue
        first=True
        for t,start,end in spans:
            a=max(start,match.start()); b=min(end,match.end())
            if a<b:
                s=t.text or ''
                t.text=s[:a-start]+(repl if first else '')+s[b-start:]
                first=False
        count+=1
    return count

def new_p(template,text,pid=None):
    p=copy.deepcopy(template)
    rpr=template.find('.//w:r/w:rPr',NS)
    for child in list(p):
        if child.tag!=W+'pPr':p.remove(child)
    if pid:p.set('{'+NS['w14']+'}paraId',pid)
    r=E.SubElement(p,W+'r')
    if rpr is not None:r.append(copy.deepcopy(rpr))
    t=E.SubElement(r,W+'t');t.text=text
    if text[:1].isspace() or text[-1:].isspace():t.set('{http://www.w3.org/XML/1998/namespace}space','preserve')
    return p

def norm(el):
    c=copy.deepcopy(el)
    for t in c.iter(W+'t'):
        if t.text:t.text=CITE.sub('[CITATION]',t.text)
    return E.tostring(c,method='c14n')

def run(source,output,report):
    data=pathlib.Path(source).read_bytes()
    assert blobsha(data)==DATA['source_sha'], 'Source DOCX changed: refusing to overwrite.'
    with zipfile.ZipFile(source) as zin:
        root=E.fromstring(zin.read('word/document.xml'))
        body=root.find('w:body',NS); original_children=list(body)
        paras=body.findall('w:p',NS)
        rw=next(p for p in paras if txt(p).startswith('2 相关工作'))
        method=next(p for p in paras if txt(p)=='3 方法')
        rh=next(p for p in paras if txt(p).startswith('参考文献'))
        rwi,mi,rhi=map(body.index,(rw,method,rh))
        protected=original_children[:rwi]+original_children[mi:rhi]
        protected_norm=[norm(p) for p in protected]
        old_refs={}; old_ref_nodes=[]
        for p in original_children[rhi+1:]:
            m=re.match(r'^\[(\d+)\]\s*(.+)$',txt(p))
            if m:old_refs[int(m[1])]=m[2];old_ref_nodes.append(p)
        assert len(old_refs)==35
        old_refs.update({int(k):v for k,v in DATA['reference_updates'].items()})
        original_headings={txt(p):p for p in original_children[rwi+1:mi] if p.find('w:pPr/w:pStyle',NS) is not None}
        paragraph_template=original_children[rwi+2]
        new_related=[new_p(rw,'2 相关工作')]
        pid=0x6000A000
        for sec in DATA['sections']:
            new_related.append(copy.deepcopy(original_headings[sec['heading']]))
            for s in sec['paragraphs']:
                pid+=1;new_related.append(new_p(paragraph_template,s,f'{pid:08X}'))
        for child in original_children[rwi:mi]:body.remove(child)
        for i,p in enumerate(new_related):body.insert(rwi+i,p)
        # Traverse all body text, including table cells and inserted revision text.
        cite_paras=[]
        for child in body:
            if child is rh:break
            if child.tag==W+'p':cite_paras.append(child)
            cite_paras.extend(child.findall('.//w:p',NS))
        order=[]
        for p in cite_paras:
            for match in CITE.finditer(''.join(t.text or '' for t in paragraph_nodes(p))):
                for n in refnums(match):
                    assert n in old_refs, f'Unresolved reference {n}'
                    if n not in order:order.append(n)
        mapping={old:i+1 for i,old in enumerate(order)}
        changed=sum(replace_citations(p,mapping) for p in cite_paras)
        assert [norm(p) for p in protected]==protected_norm, 'Non-citation content outside related work changed.'
        template=old_ref_nodes[0]
        for p in old_ref_nodes:body.remove(p)
        for i,old in enumerate(order):
            body.insert(body.index(rh)+1+i,new_p(template,f'[{i+1}] '+old_refs[old],f'{0x6100A001+i:08X}'))
        visible_refs=[]
        for p in cite_paras:
            for match in CITE.finditer(''.join(t.text or '' for t in paragraph_nodes(p))):visible_refs.extend(refnums(match))
        assert set(visible_refs)==set(range(1,len(order)+1))
        assert len(order)==27, f'Unexpected reference total {len(order)}'
        newxml=E.tostring(root,encoding='UTF-8',xml_declaration=True,standalone=True)
        with zipfile.ZipFile(output,'w') as zout:
            for info in zin.infolist():
                zout.writestr(copy.copy(info),newxml if info.filename=='word/document.xml' else zin.read(info.filename))
            zout.comment=zin.comment
        other_parts=[]
        with zipfile.ZipFile(output) as zout:
            assert zout.namelist()==zin.namelist()
            for name in zin.namelist():
                if name!='word/document.xml':
                    assert zin.read(name)==zout.read(name),f'Unexpected package change: {name}'
                    other_parts.append(name)
    result={'source_blob_sha':blobsha(data),'output_blob_sha':blobsha(pathlib.Path(output).read_bytes()),
      'document_xml_sha256':hashlib.sha256(newxml).hexdigest(),
      'reference_count_before':35,'reference_count_after':len(order),'reference_map':mapping,
      'removed_reference_numbers':[n for n in range(1,36) if n not in mapping],
      'new_reference_numbers':[mapping[n] for n in order if n>35],
      'citation_groups_renumbered':changed,'all_citations_resolve':True,
      'non_related_content_preserved':True,'unchanged_package_parts':other_parts,
      'related_body_characters':sum(len(x) for s in DATA['sections'] for x in s['paragraphs']),
      'tables':len(root.findall('.//w:tbl',NS)),'equations':len(root.findall('.//m:oMath',NS))}
    pathlib.Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('output');ap.add_argument('--report',default='audit.json')
    args=ap.parse_args();run(args.source,args.output,args.report)
