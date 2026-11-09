/**
 * @license Copyright (c) 2003-2014, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For the complete reference:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

	// The toolbar groups arrangement, optimized for a single toolbar row.
	config.toolbarGroups = [
		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
		{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
		{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
		{ name: 'forms' },
		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
		{ name: 'links' },
		{ name: 'insert' },
		{ name: 'styles' },
		{ name: 'colors' },
		{ name: 'tools' },
		{ name: 'others' },
		{ name: 'about' }
	];

	// The default plugins included in the basic setup define some buttons that
	// we don't want too have in a basic editor. We remove them here.
	config.removeButtons = 'Cut,Copy,Paste,Undo,Redo,Anchor,Underline,Strike,Subscript,Superscript';

	// Let's have it basic on dialogs as well.
	config.removeDialogTabs = 'link:advanced';

	// ckeditor.js is the 4.22.1 standard build; only enable the plugins of the
	// previous custom basic build (basic preset + Paste from Word).
	config.plugins = 'basicstyles,enterkey,entities,floatingspace,wysiwygarea,' +
		'indent,indentlist,dialogui,dialog,fakeobjects,link,list,button,toolbar,' +
		'clipboard,pastefromword';

	// Only lang/en.js and the moono skin are shipped.
	config.language = 'en';
	config.skin = 'moono';

	// 4.22.1 is the last open-source release (4.23+ is commercial LTS). Its
	// version check would warn every user and call cdn.ckeditor.com.
	config.versionCheck = false;
};
