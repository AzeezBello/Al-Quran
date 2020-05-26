from django.shortcuts import get_list_or_404, get_object_or_404, render
from quran.models import *


def index(request):
    suras = get_list_or_404(Sura)
    return render(request, 'quran/index.html', {'suras': suras})


def sura(request, sura_number, translation=1):
    sura = get_object_or_404(Sura, number=sura_number)
    ayas = sura.ayas.all()
    if translation:
        translations = sura.translations.filter(translation=translation)
        ayas = zip(ayas, translations)
    return render(request, 'quran/sura.html', {'sura': sura, 'ayas': ayas})


def aya(request, sura_number, aya_number, translation=1):
    sura = get_object_or_404(Sura, number=sura_number)
    aya = get_object_or_404(Aya, sura=sura, number=aya_number)
    translated_aya = get_object_or_404(TranslatedAya, aya=aya, translation=translation)
    words = aya.words.all()
    return render(request, 'quran/aya.html', {'sura': sura, 'aya': aya, 'translation': translated_aya, 'words': words})


def word(request, sura_number, aya_number, word_number):
    aya = get_object_or_404(Aya, sura=sura_number, number=aya_number)
    word = get_object_or_404(Word, aya=aya, number=word_number)
    root = word.root
    return render(request, 'quran/word.html', {'word': word, 'aya': aya, 'root': root})


def lemma(request, lemma_id):
    lemma = get_object_or_404(Lemma, pk=lemma_id)
    root = lemma.root
    words = lemma.word_set.all()
    ayas = lemma.ayas.distinct()
    return render(request, 'quran/lemma.html', {'lemma': lemma, 'root': root, 'words': words, 'ayas': ayas})


def root(request, root_id):
    root = get_object_or_404(Root, pk=root_id)
    lemmas = root.lemmas.all()
    ayas = root.ayas.distinct()
    return render(request, 'quran/root.html', {'root': root, 'lemmas': lemmas, 'ayas': ayas})


def root_index(request):
    roots = Root.objects.all().order_by('letters')
    return render(request, 'quran/root_index.html', {'roots': roots})