import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeadComponent } from './head/head.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {FlexLayoutModule} from '@angular/flex-layout';
import { MatTabsModule, MatMenuModule,MatFormFieldModule,MatSidenavModule, MatToolbarModule ,MatIconModule,MatListModule , MatButtonModule} from '@angular/material';
import { HeaderComponent } from './navigation/header/header.component';
import { SidenavListComponent } from './navigation/sidenav-list/sidenav-list.component';
import { FixedsidnavComponent } from './fixedsidnav/fixedsidnav.component';
import { AboutUsComponent } from './about-us/about-us.component';
import {HttpClientModule} from '@angular/common/http';
import { UploadImageComponent } from './upload-image/upload-image.component';
import { ElementsComponent } from './elements/elements.component';
import { FileSelectDirective } from 'ng2-file-upload';
import { FormsModule } from '@angular/forms';



@NgModule({
  declarations: [
    AppComponent,
    HeadComponent,
    HeaderComponent,
    SidenavListComponent,
    FixedsidnavComponent,
    AboutUsComponent,
    UploadImageComponent,
    ElementsComponent,
    FileSelectDirective

  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FlexLayoutModule,
    MatTabsModule,
     MatSidenavModule,
     MatToolbarModule,
     MatIconModule,
      MatButtonModule,
      MatListModule,
      HttpClientModule,
      MatMenuModule,
      FormsModule,
      MatFormFieldModule
  ],
  exports:[
    MatTabsModule,
    MatSidenavModule,
     MatToolbarModule,
     MatIconModule,
     MatButtonModule,
     MatListModule,
     HttpClientModule,
     MatMenuModule,
     MatFormFieldModule
    ],

  providers: [
    UploadImageComponent
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
